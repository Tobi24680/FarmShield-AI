
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best.onnx"
ALERTS_DIR      = BASE_DIR / "alerts"
SCREENSHOTS_DIR = ALERTS_DIR / "screenshots"
ALERT_LOG_PATH  = ALERTS_DIR / "alert_log.csv"

# Ensure directories exist
ALERTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

CLASS_NAMES = ["Bear", "Boar", "Elephant"]


INPUT_WIDTH  = 640
INPUT_HEIGHT = 640
CONF_THRESHOLD = 0.30

CLASS_COLORS = {
    0: (60,  20, 220),   # Bear     – deep red-violet
    1: (34, 139,  34),   # Boar     – forest green
    2: (255, 140,   0),  # Elephant – vivid orange
}

# ── Alert Cooldown ──────────────────────────────────────
ALERT_COOLDOWN_SECONDS = 6   # Min seconds between alerts during live stream
