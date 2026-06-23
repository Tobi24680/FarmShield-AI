"""
FarmShield AI – Alert Manager
Saves annotated screenshots and logs detections to CSV.
"""

import csv
from datetime import datetime

import cv2

from app.config import ALERT_LOG_PATH, SCREENSHOTS_DIR


# ─────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────

def _ensure_log_headers():
    """Create alert_log.csv with headers if it does not exist."""
    if not ALERT_LOG_PATH.exists():
        with open(ALERT_LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "animals_detected", "screenshot_path"])


def _append_log(timestamp_str: str, animals_str: str, screenshot_name: str):
    """Append one detection row to the CSV alert log."""
    _ensure_log_headers()
    with open(ALERT_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp_str, animals_str, screenshot_name])


# ─────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────

def save_alert(image_bgr, detected_animals: list) -> str:
    """
    Save annotated screenshot and log the detection to CSV.

    Parameters
    ----------
    image_bgr        : numpy BGR image with bounding boxes already drawn
    detected_animals : list of class name strings, e.g. ['Elephant', 'Bear']

    Returns
    -------
    str  Formatted alert message to display in the Gradio UI
    """
    now       = datetime.now()
    time_str  = now.strftime("%Y-%m-%d %H:%M:%S")
    file_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    unique_animals = sorted(set(detected_animals))
    animal_tag     = "_".join(a.lower() for a in unique_animals)
    filename       = f"{animal_tag}_{file_time}.jpg"
    filepath       = SCREENSHOTS_DIR / filename

    # Save annotated screenshot
    cv2.imwrite(str(filepath), image_bgr)

    # Append to CSV log
    animals_str = ", ".join(unique_animals)
    _append_log(time_str, animals_str, filename)

    # Build alert message for UI
    alert_lines = [
        "⚠️  ALERT TRIGGERED",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🐾  Animal(s) Detected : {animals_str}",
        f"🕐  Time               : {time_str}",
        f"📸  Screenshot Saved   : {filename}",
        f"📁  Location           : alerts/screenshots/",
    ]

    return "\n".join(alert_lines)