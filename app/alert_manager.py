import cv2
import csv
import time
from pathlib import Path
from datetime import datetime

from app.config import (
    ALERTS_DIR,
    SCREENSHOTS_DIR,
    ALERT_LOG_PATH,
    ALERT_COOLDOWN_SECONDS,
)

ALERTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# ── Cooldown tracker ──────────────────────────────────
_last_alert_time: float = 0.0


def _can_alert() -> bool:
    """Return True if enough time has elapsed since the last alert."""
    global _last_alert_time
    now = time.time()
    if now - _last_alert_time >= ALERT_COOLDOWN_SECONDS:
        _last_alert_time = now
        return True
    return False


def _write_csv_row(timestamp_str: str, animals: str, filename: str, confidences: str):
    """Append one row to the CSV log, creating the file with headers if needed."""
    file_exists = ALERT_LOG_PATH.exists()
    with open(ALERT_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Animals", "Confidences", "Screenshot"])
        writer.writerow([timestamp_str, animals, confidences, filename])


def save_alert(image, detected_animals, confidences=None):
    """Save alert screenshot + CSV log and return a formatted alert string.

    Parameters
    ----------
    image : np.ndarray
        Annotated BGR image from YOLO.
    detected_animals : list[str]
        List of class names detected.
    confidences : list[float] | None
        Corresponding confidence values (0-1).
    """
    if not detected_animals:
        return "✅ No Wildlife Detected\n━━━━━━━━━━━━━━━━━━━━━━━━━━\nYour farm area appears safe.\nNo animals (Bear, Boar, Elephant) were found in this image."

    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    save_path = SCREENSHOTS_DIR / filename

    # Save annotated image
    cv2.imwrite(str(save_path), image)

    animals_str = ", ".join(set(detected_animals))
    conf_str = ""
    if confidences:
        conf_str = ", ".join(f"{c:.0%}" for c in confidences)

    # Log to CSV
    _write_csv_row(timestamp_str, animals_str, filename, conf_str)

    alert = (
        f"⚠️ ALERT TRIGGERED\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🐾 Animal(s) Detected : {animals_str}\n"
        f"📊 Confidence         : {conf_str if conf_str else 'N/A'}\n"
        f"🕐 Time               : {timestamp_str}\n"
        f"📸 Screenshot Saved   : {filename}\n"
        f"📁 Location           : alerts/screenshots/"
    )
    return alert


def save_alert_live(image, detected_animals, confidences=None):
    """Same as save_alert but respects the cooldown timer.

    Returns the alert string if an alert was fired, or a short status
    string if the cooldown hasn't expired yet.
    """
    if not detected_animals:
        return (
            "🟢 MONITORING — No wildlife detected\n"
            "System is actively scanning..."
        )

    if not _can_alert():
        animals_str = ", ".join(set(detected_animals))
        return (
            f"🔴 LIVE DETECTION — {animals_str}\n"
            "Alert cooldown active. Monitoring continues..."
        )

    # Full alert with save
    return save_alert(image, detected_animals, confidences)