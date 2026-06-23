"""
FarmShield AI – Configuration
Central config for paths, model settings, class names, and alert thresholds.
"""

from pathlib import Path

# ─────────────────────────────────────────────
# Base paths
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best.onnx"

ALERTS_DIR      = BASE_DIR / "alerts"
SCREENSHOTS_DIR = ALERTS_DIR / "screenshots"
ALERT_LOG_PATH  = ALERTS_DIR / "alert_log.csv"

# Auto-create directories if missing
ALERTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# Model settings
# ─────────────────────────────────────────────
CLASS_NAMES = ["Bear", "Boar", "Elephant"]

# Input size expected by the ONNX model
INPUT_WIDTH  = 640
INPUT_HEIGHT = 640

# Confidence threshold for detections
CONF_THRESHOLD = 0.30

# ─────────────────────────────────────────────
# Per-class bounding box colors (BGR)
# ─────────────────────────────────────────────
CLASS_COLORS = {
    0: (60,  20, 220),   # Bear     – deep red-violet
    1: (34, 139,  34),   # Boar     – forest green
    2: (255, 140,   0),  # Elephant – vivid orange
}