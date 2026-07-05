# FarmShield AI 🌾 – Wildlife Intrusion Detection & Alert System

[![HuggingFace Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Space-blue)](https://huggingface.co/spaces)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![ONNX Runtime](https://img.shields.io/badge/ONNX-Runtime-orange)](https://onnxruntime.ai)
[![Gradio](https://img.shields.io/badge/Gradio-UI-blueviolet)](https://gradio.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **FarmShield AI** is an end-to-end wildlife intrusion detection system built for smart agriculture.  
> Upload a farm field image (or use your webcam) and the system will instantly detect **Bear**, **Boar**, or **Elephant** using a custom-trained YOLO ONNX model — then generate a timestamped alert and save an annotated screenshot.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 Animal Detection | Bear · Boar · Elephant (3-class YOLOv8) |
| ⚡ Inference Engine | ONNX Runtime (CPU, no GPU required) |
| 📷 Input Methods | Image upload · Live webcam |
| 🚨 Alert System | Popup notifications + Gradio warnings |
| 🎤 Tamil Voice Alerts | Natural speech synthesis with gTTS + pygame |
| 📸 Auto Screenshot | Saved to `alerts/screenshots/` with timestamp |
| 📋 CSV Log | All detections logged to `alerts/alert_log.csv` |
| 🎨 Premium UI | Gradio Blocks with dark agri-green glassmorphism theme |
| ⚡ Ultra-Low Latency | Real-time webcam streaming |
| 🤗 HuggingFace Ready | Deploys to Spaces with zero changes |
| 🎪 Multi-Modal Alerts | Popup + Banner + Alarm sound + Tamil voice |

---

## 🗂 Project Structure

```
FarmShield/
│
├── app/
│   ├── __init__.py          # Package init
│   ├── config.py            # Paths, class names, thresholds
│   ├── alert_manager.py     # Screenshot saving + CSV logging
│   ├── onnx_predict.py      # ONNX inference + drawing
│   └── gradio_app.py        # Gradio Blocks UI
│
├── models/
│   └── best.onnx            # Your trained YOLO model (not included in repo)
│
├── alerts/
│   ├── screenshots/         # Auto-saved detection images
│   └── alert_log.csv        # Auto-created detection log
│
├── main.py                  # Entry point
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/FarmShield-AI.git
cd FarmShield-AI
```

### 2. Create environment & install dependencies

**Using `uv` (recommended - fastest):**
```bash
pip install uv
uv sync
```

**Or manually with uv pip:**
```bash
pip install uv
uv venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
uv pip install -r requirements.txt
```

**Using plain pip:**
```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Add your model
Place your exported ONNX model at:
```
models/best.onnx
```

### 4. Run the app
```bash
python main.py
```
Then open `http://localhost:7860` in your browser.

---

## 🎯 Input Methods

### 1. 📤 Upload Image
Upload a JPG/PNG image of your farm field for instant detection.

### 2. 📹 Live Webcam
Stream directly from your webcam with real-time bounding boxes and alerts.

### 3. 📹 Live Webcam Stream
Native Gradio webcam streaming for real-time detections:
- **No extra WebRTC dependency** – works with Gradio 6.19
- **Real-time detection** – frame-by-frame analysis
- **Adjustable threshold** – confidence slider
- **Perfect for 24/7 monitoring** – ideal for farm surveillance

---

## 🎤 Tamil Voice Alerts

When an animal is detected, FarmShield AI generates **natural Tamil speech**:

- **Automatic speech synthesis** using Google Text-to-Speech (gTTS)
- **Non-blocking playback** – doesn't freeze the UI
- **Multi-lingual ready** – easily extensible to other languages
- **Example alert:**
  ```
  எச்சரிக்கை! உங்கள் வயலில் யானை, கரடி கண்டறியப்பட்டுள்ளது। 
  தயவுசெய்து வயலுக்குள் செல்ல வேண்டாம். பாதுகாப்பாக இருங்கள்.
  
  Translation: "Alert! Elephant and bear detected in your field. 
  Please don't enter the field. Stay safe."
  ```

---

## 🚨 Multi-Layer Alert System

When an animal is detected, **all alert systems activate simultaneously:**

1. **🎤 Tamil Voice** – Natural speech via gTTS + pygame
2. **📢 Popup Notification** – Gradio warning popup on screen
3. **🔊 Alarm Sound** – Web Audio API siren (3 beeps)
4. **🚨 Banner** – Red alert banner at top of page
5. **📸 Screenshot** – Auto-saved with timestamp
6. **📋 CSV Log** – Logged for records & analytics

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Architecture | YOLOv8 (Ultralytics) |
| Export format | ONNX |
| Input shape | `[1, 3, 640, 640]` |
| Output shape | `[1, 300, 6]` |
| Output format | `[x1, y1, x2, y2, score, class_id]` |
| Confidence threshold | 0.30 |

### Class Mapping

| ID | Animal | Box Colour |
|---|---|---|
| 0 | 🐻 Bear | Deep violet |
| 1 | 🐗 Boar | Forest green |
| 2 | 🐘 Elephant | Vivid orange |

---

## 📊 Alert Logging

### CSV Log Format
All detections are automatically saved to `alerts/alert_log.csv`:

```csv
Timestamp,Animals,Confidences,Screenshot
2026-07-04 14:30:15,Elephant,95%,20260704_143015.jpg
2026-07-04 14:35:42,Bear,87%,20260704_143542.jpg
2026-07-04 15:10:08,Boar,92%,20260704_151008.jpg
```

### Screenshot Directory
All annotated images are saved with bounding boxes to `alerts/screenshots/`

---

## ❓ Troubleshooting

### Issue: Live webcam not working
- Ensure Gradio 6.19 is installed: `pip install gradio==6.19.0`
- Check browser compatibility (Chrome/Edge recommended)
- Ensure your camera permissions are granted

### Issue: Tamil voice not playing
- Verify `gtts` and `pygame` are installed
- Check internet connection (gTTS requires it)
- Ensure speakers are not muted
- For Linux: install `pulseaudio` or `alsa`

### Issue: ONNX model not found
- Place your trained model at `models/best.onnx`
- Verify the path in `app/config.py`
- Check file permissions

### Issue: High CPU usage
- Reduce inference frequency in `app/config.py`
- Increase `CONF_THRESHOLD` to reduce detections
- Use OpenCV headless version (already in requirements)

---

## 📸 Alert Example

```
⚠️  ALERT TRIGGERED
━━━━━━━━━━━━━━━━━━━━━━━━━━
🐾  Animal(s) Detected : Elephant
🕐  Time               : 2026-06-23 12:10:33
📸  Screenshot Saved   : elephant_2026-06-23_12-10-33.jpg
📁  Location           : alerts/screenshots/
```

---

## 🛠 Tech Stack

### Core AI & Detection
- **Python 3.10+**
- **YOLOv26 (Ultralytics)** – Object detection
- **ONNX Runtime** – CPU-optimized inference
- **NumPy** – Array operations
- **OpenCV** – Image processing & bounding boxes

### Web UI & Streaming
- **Gradio 6.19.0** – Interactive web interface
- **Pillow** – Image handling
- **Gradio Blocks** – Custom component layout

### Audio & Alerts
- **gTTS** – Google Text-to-Speech (Tamil)
- **pygame** – Audio playback
- **Web Audio API** – Browser alarm sounds

### Package Management
- **uv** – Fast Python package installer (optional but recommended)

---

## 📦 Dependencies

All dependencies are in `pyproject.toml`:

```toml
dependencies = [
    "gradio==6.19.0",
    "onnxruntime>=1.18.0",
    "opencv-python-headless>=4.9.0",
    "numpy>=1.26.0",
    "ultralytics>=8.0.0",
    "gtts>=2.4.0",          # Tamil voice alerts
    "pygame>=2.5.0",        # Audio playback
]
```

---

## 👩‍💻 Author & Contact

Built by **SHREERAM M K**  
📧 **Email:** sumathidevan2006@gmail.com  
📱 **Phone:** +91 9087418802  
🔗 **GitHub:** [github.com/Tobi24680](https://github.com/Tobi24680)  
🎓 **Institution:** Annamalai University, CSE - AI & ML

---

## 🌟 Project Vision

**FarmShield AI** aims to:
- ✅ Bring affordable AI-based wildlife monitoring to farms
- ✅ Reduce crop losses from wildlife intrusions
- ✅ Improve farmer safety through instant alerts
- ✅ Build a scalable smart agriculture security platform
- ✅ Support local languages (Tamil, Telugu, etc.) for accessibility

---

## 📄 License

MIT License – free to use, modify, and distribute.
