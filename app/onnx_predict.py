import cv2
import numpy as np
from pathlib import Path
from PIL import Image as PILImage
from ultralytics import YOLO
import gradio as gr
import threading
import tempfile
import os
from app.config import MODEL_PATH, CONF_THRESHOLD
from app.alert_manager import save_alert, save_alert_live

# Import gTTS and pygame for Tamil voice alerts
try:
    from gtts import gTTS
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


model = YOLO(str(MODEL_PATH), task="detect")

def generate_tamil_audio(animal_list):
    """Generate Tamil voice alert for detected animals using gTTS.
    
    Returns:
    --------
    str : Path to the generated MP3 file, or None if failed.
    """
    if not AUDIO_AVAILABLE:
        print("⚠️ Audio system not available (gTTS/pygame not installed)")
        return None

    # Convert list to string if needed
    if isinstance(animal_list, list):
        animal_list = ", ".join(animal_list)

    # Tamil animal names mapping
    animal_names_tamil = {
        "elephant": "யானை",
        "bear": "கரடி",
        "boar": "காட்டுப்பன்றி",
    }

    # Replace English names with Tamil
    tamil_animals = []
    for animal in animal_list.split(","):
        animal = animal.strip().lower()
        tamil_name = animal_names_tamil.get(animal, animal)
        tamil_animals.append(tamil_name)

    tamil_animal_str = ", ".join(tamil_animals)

    # Tamil alert message
    if animal_list == "safe":
        tamil_text = "எந்த விலங்கும் கண்டறியப்படவில்லை. நீங்கள் பாதுகாப்பாக வயலுக்குச் செல்லலாம்."
    else:
        tamil_text = (
            f"எச்சரிக்கை! உங்கள் வயலில் {tamil_animal_str} கண்டறியப்பட்டுள்ளது. "
            "தயவுசெய்து வயலுக்குள் செல்ல வேண்டாம். பாதுகாப்பாக இருங்கள்."
        )

    try:
        # Generate speech using gTTS
        tts = gTTS(text=tamil_text, lang="ta", slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name

        tts.save(temp_filename)
        return temp_filename
    except Exception as e:
        print(f"❌ Tamil voice alert error: {e}")
        return None


def predict_image(image, conf_threshold=None):
    """Run detection on an uploaded image.

    Returns (annotated_image, alert_string).
    - If detections found  → alert string contains 'ALERT TRIGGERED' (triggers JS alarm)
    - If nothing detected  → friendly 'no detection' message
    """
    if image is None:
        return None, ""

    if conf_threshold is None:
        conf_threshold = CONF_THRESHOLD

    results = model.predict(image, conf=conf_threshold)

    names = []
    confidences = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        names.append(model.names[cls])
        confidences.append(conf)

    annotated = results[0].plot()

    audio_path = None
    if names:
        unique_animals = ", ".join(set(names))
        gr.Warning(f"🚨 Wildlife Alert! {unique_animals} detected in your farm field. Stay away and remain safe.")
        audio_path = generate_tamil_audio(unique_animals)
        alert = save_alert(annotated, names, confidences)
    else:
        gr.Info("✅ Safe: No wildlife detected.")
        alert = (
            "✅ No Wildlife Detected\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Your farm area appears safe.\n"
            "No animals (Bear, Boar, Elephant) were found in this image."
        )
        audio_path = generate_tamil_audio("safe")

    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return annotated, alert, audio_path


def predict_webcam_frame(frame, conf_threshold=None):
    """Run detection on a single webcam frame.

    Draws bounding boxes with class-coloured labels and confidence
    directly on the frame.  Uses `save_alert_live` which respects
    the cooldown timer so alerts aren't spammed every frame.

    Returns (annotated_frame, alert_string).
    """
    if frame is None:
        return None, ""

    if conf_threshold is None:
        conf_threshold = CONF_THRESHOLD

    results = model.predict(frame, conf=conf_threshold, verbose=False)

    names = []
    confidences = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        names.append(model.names[cls])
        confidences.append(conf)

    annotated = results[0].plot()

    alert = save_alert_live(annotated, names, confidences)
    
    # Play Tamil alert only on first detection (when alert is triggered)
    if names and alert.startswith("⚠️ ALERT TRIGGERED"):
        unique_animals = ", ".join(set(names))
        # Play Tamil voice alert in background thread
        threading.Thread(
            target=play_tamil_alert,
            args=(unique_animals,),
            daemon=True
        ).start()
    elif not names and alert.startswith("✅"):
        # If cooldown for safe message is implemented, it would go here.
        # For live stream, spamming "safe" every frame is bad, so we only play it if state changed from danger to safe.
        pass

    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return annotated, alert


def predict_webrtc_stream(frame, conf_threshold=None):
    """Real-time WebRTC detection with class annotations.
    
    Optimized for continuous streaming with minimal latency.
    Returns annotated frame with bounding boxes and class labels.
    
    Parameters:
    -----------
    frame : np.ndarray
        Input frame from WebRTC stream (BGR format)
    conf_threshold : float, optional
        Confidence threshold for detection
        
    Returns:
    --------
    np.ndarray
        Annotated frame with detection bounding boxes and labels
    """
    if frame is None:
        return frame

    # fastrtc sometimes passes (image, audio) tuple
    if isinstance(frame, tuple):
        frame = frame[0]

    if conf_threshold is None:
        conf_threshold = CONF_THRESHOLD

    # Run detection
    results = model.predict(frame, conf=conf_threshold, verbose=False)
    
    # Extract detection info
    names = []
    confidences = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        names.append(model.names[cls])
        confidences.append(conf)

    # Plot bounding boxes and labels
    annotated = results[0].plot()
    
    alert_msg = gr.skip()
    audio_path = gr.skip()

    # Alert management with cooldown
    if names:
        # Try to trigger alert respecting cooldown timer
        live_alert = save_alert_live(annotated, names, confidences)
        # Trigger audio and popup only on first detection (when alert is triggered)
        if live_alert.startswith("⚠️ ALERT TRIGGERED"):
            unique_animals = ", ".join(set(names))
            gr.Warning(f"🚨 WebRTC: {unique_animals} detected! Stay away!")
            audio_path = generate_tamil_audio(unique_animals)
            alert_msg = live_alert
    else:
        # For webrtc, to avoid audio spam, we don't play safe on every frame.
        pass

    # Convert BGR (from plot()) to RGB for WebRTC component
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    return annotated, alert_msg, audio_path
