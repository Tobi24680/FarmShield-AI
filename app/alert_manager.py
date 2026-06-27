import cv2
from pathlib import Path
from datetime import datetime

SAVE_DIR = Path("alerts")
SAVE_DIR.mkdir(exist_ok=True)


def save_alert(image, detected_animals):
    # Create filename using current time
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    # Save annotated image
    cv2.imwrite(str(SAVE_DIR / filename), image)

    # Return simple message
    if detected_animals:
        animals = ", ".join(set(detected_animals))
        return f"⚠️ ALERT TRIGGERED\nDetected: {animals}\nSaved: {filename}"
    else:
        return "No animal detected."