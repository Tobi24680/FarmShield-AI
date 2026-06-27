import cv2
import numpy as np
from pathlib import Path
from PIL import Image as PILImage
from ultralytics import YOLO
from app.config import MODEL_PATH, CONF_THRESHOLD
from app.alert_manager import save_alert


model = YOLO(str(MODEL_PATH))

def predict_image(image, conf_threshold=None):
    if conf_threshold is None:
        conf_threshold = 0.4

    results = model.predict(image, conf=conf_threshold)

    annotated = results[0].plot()

    names = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        names.append(model.names[cls])

    if names:
        alert = save_alert(annotated, names)
    else:
        alert = "No animal detected."

    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return annotated, alert


def monitor_webcam(source=0, show=True, stream=True, conf_threshold=None):
    """Run live webcam monitoring using Ultralytics YOLO."""
    if conf_threshold is None:
        conf_threshold = CONF_THRESHOLD

    print("Starting live webcam monitor. Press Ctrl+C to stop.")
    results = model.predict(
        source=source,
        show=show,
        stream=stream,
        conf=conf_threshold,
    )

    for result in results:
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            print("No animal detected.")
            continue

        print("Detected boxes:")
        for box in boxes:
            print(box)

    return None


