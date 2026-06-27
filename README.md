# FarmShield AI 🌾 – Wildlife Intrusion Detection & Alert System

[![HuggingFace Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Space-blue)](https://huggingface.co/spaces)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![ONNX Runtime](https://img.shields.io/badge/ONNX-Runtime-orange)](https://onnxruntime.ai)
[![Gradio](https://img.shields.io/badge/Gradio-UI-blueviolet)](https://gradio.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **FarmShield AI** is an end-to-end wildlife intrusion detection system built for smart agriculture.  
> Upload a farm field image (or use your webcam) and the system will instantly detect **Bear**, **Boar**, or **Elephant** using a custom-trained YOLO ONNX model — then generate a timestamped alert and save an annotated screenshot.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 Animal Detection | Bear · Boar · Elephant |
| ⚡ Inference Engine | ONNX Runtime (CPU, no GPU required) |
| 📷 Image Sources | File upload + live webcam capture |
| 🚨 Alert System | Timestamped alert message in UI |
| 📸 Auto Screenshot | Saved to `alerts/screenshots/` |
| 📋 CSV Log | All detections logged to `alerts/alert_log.csv` |
| 🎨 Premium UI | Gradio Blocks with dark agri-green theme |
| 🤗 HuggingFace Ready | Deploys to Spaces with zero changes |

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

**Using `uv` (recommended):**
```bash
pip install uv
uv venv
uv pip install -r requirements.txt
```

**Using plain pip:**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
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

- **Python 3.10+**
- **Gradio** – interactive web UI
- **ONNX Runtime** – CPU inference
- **OpenCV** – image processing & bounding boxes
- **Pillow** – PIL image handling
- **NumPy** – array operations

---

## 👩‍💻 Author

Built by **SHREERAM M K** as a portfolio  project.  
Demonstrates end-to-end AI deployment: model training → ONNX export → inference pipeline → production UI.

---

## 📄 License

MIT License – free to use, modify, and distribute.
