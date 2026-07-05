import cv2
from ultralytics import YOLO
import gradio as gr
import tempfile
from app.config import MODEL_PATH, CONF_THRESHOLD
from app.alert_manager import save_alert, save_alert_live

# Import gTTS for Tamil voice alerts (audio is played client-side via gr.Audio)
try:
    from gtts import gTTS
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False


model = YOLO(str(MODEL_PATH), task="detect")

def generate_tamil_audio(animal_list):
    """Generate a Tamil voice alert MP3 and return the file path."""

    if not AUDIO_AVAILABLE:
        print("⚠️ Audio system not available (gTTS not installed)")
        return None

    if isinstance(animal_list, list):
        animal_list = ", ".join(animal_list)

    animal_names_tamil = {
        "elephant": "யானை",
        "bear": "கரடி",
        "boar": "காட்டுப்பன்றி",
    }

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
    Returns: (annotated_image, alert_text, audio_filepath_or_None)
    """

    if image is None:
        return None, "", None

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

    audio_file = None

    if names:
        unique_animals = ", ".join(set(names))
        gr.Warning(f"🚨 Wildlife Alert! {unique_animals} detected in your farm field. Stay away and remain safe.")
        # Generate Tamil voice alert MP3 (will be played client-side)
        audio_file = generate_tamil_audio(unique_animals)
        alert = save_alert(annotated, names, confidences)
    else:
        gr.Info("✅ Safe: No wildlife detected.")
        alert = (
            "✅ No Wildlife Detected\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Your farm area appears safe.\n"
            "No animals (Bear, Boar, Elephant) were found in this image."
        )
        # Generate Tamil "safe" voice alert MP3 (will be played client-side)
        audio_file = generate_tamil_audio("safe")

    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return annotated, alert, audio_file


def predict_webcam_frame(frame, conf_threshold=None):
    """Run detection on a live webcam frame.
    Returns: (annotated_frame, alert_text, audio_filepath_or_None)
    """

    if frame is None:
        return None, "", None

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

    audio_file = None

    if names and alert.startswith("⚠️ ALERT TRIGGERED"):
        unique_animals = ", ".join(set(names))
        # Generate Tamil voice alert MP3 (will be played client-side)
        audio_file = generate_tamil_audio(unique_animals)
    elif not names and alert.startswith("✅"):
        # If cooldown for safe message is implemented, it would go here.
        # For live stream, spamming "safe" every frame is bad, so we only play it if state changed from danger to safe.
        pass

    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    return annotated, alert, audio_file


def predict_webrtc_stream(frame, conf_threshold=None):
    return predict_webcam_frame(frame, conf_threshold)
