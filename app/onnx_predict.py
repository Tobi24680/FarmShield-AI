"""
FarmShield AI – ONNX Inference Engine
Handles model loading, pre/post-processing, bounding-box drawing, and prediction.
"""

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

from app.config import (
    MODEL_PATH,
    CLASS_NAMES,
    CLASS_COLORS,
    CONF_THRESHOLD,
    INPUT_WIDTH,
    INPUT_HEIGHT,
)
from app.alert_manager import save_alert


class FarmShieldONNX:
    """ONNX-Runtime inference wrapper for the FarmShield wildlife detector."""

    def __init__(self):
        self.session = ort.InferenceSession(
            str(MODEL_PATH),
            providers=["CPUExecutionProvider"],
        )
        inp              = self.session.get_inputs()[0]
        self.input_name  = inp.name
        self.output_names = [o.name for o in self.session.get_outputs()]

        shape              = inp.shape
        self.input_height  = int(shape[2]) if shape[2] else INPUT_HEIGHT
        self.input_width   = int(shape[3]) if shape[3] else INPUT_WIDTH

        print(
            f"[FarmShield] Model loaded | input: "
            f"{self.input_width}x{self.input_height} | classes: {CLASS_NAMES}"
        )

    # ─────────────────────────────────────────
    # Pre-processing
    # ─────────────────────────────────────────

    def preprocess(self, image_rgb: np.ndarray):
        """
        Resize → normalise → NCHW layout.

        Returns
        -------
        input_tensor : (1, 3, H, W) float32 ndarray
        orig_w, orig_h : original image dimensions
        """
        orig_h, orig_w = image_rgb.shape[:2]

        resized = cv2.resize(image_rgb, (self.input_width, self.input_height))
        blob    = resized.astype(np.float32) / 255.0
        blob    = np.transpose(blob, (2, 0, 1))           # HWC → CHW
        blob    = np.expand_dims(blob, axis=0)             # CHW → 1CHW

        return blob, orig_w, orig_h

    # ─────────────────────────────────────────
    # Post-processing
    # ─────────────────────────────────────────

    def postprocess(self, outputs, orig_w: int, orig_h: int):
        """
        Model output: (1, 300, 6)  →  [x1, y1, x2, y2, score, class_id]
        Coordinates are in model input scale (640×640); we scale back.
        """
        preds = outputs[0][0]   # shape (300, 6)

        boxes, scores, class_ids = [], [], []

        for det in preds:
            x1, y1, x2, y2, score, class_id = det

            score    = float(score)
            class_id = int(class_id)

            if score < CONF_THRESHOLD:
                continue
            if class_id < 0 or class_id >= len(CLASS_NAMES):
                continue

            # Scale coordinates back to original image size
            x1 = float(x1) * orig_w / self.input_width
            y1 = float(y1) * orig_h / self.input_height
            x2 = float(x2) * orig_w / self.input_width
            y2 = float(y2) * orig_h / self.input_height

            boxes.append([x1, y1, x2, y2])
            scores.append(score)
            class_ids.append(class_id)

        return boxes, scores, class_ids

    # ─────────────────────────────────────────
    # Drawing
    # ─────────────────────────────────────────

    def draw_detections(
        self,
        image_bgr: np.ndarray,
        boxes: list,
        scores: list,
        class_ids: list,
    ) -> np.ndarray:
        """Draw bounding boxes and labels directly on image_bgr (in-place)."""

        for box, score, cid in zip(boxes, scores, class_ids):
            x1, y1, x2, y2 = map(int, box)
            color      = CLASS_COLORS.get(cid, (0, 255, 255))
            label      = f"{CLASS_NAMES[cid]}  {score:.0%}"
            font       = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.65
            thickness  = 2

            # Filled label background
            (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            lx, ly = x1, max(y1 - th - baseline - 6, 0)
            cv2.rectangle(image_bgr, (lx, ly), (lx + tw + 8, ly + th + baseline + 6), color, -1)
            cv2.putText(
                image_bgr, label, (lx + 4, ly + th + 2),
                font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA,
            )

            # Bounding box (rounded look via two-tone border)
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), color, 3)
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (255, 255, 255), 1)

        return image_bgr

    # ─────────────────────────────────────────
    # Main prediction entry point
    # ─────────────────────────────────────────

    def predict(self, pil_image) -> tuple[Image.Image | None, str]:
        """
        Run full detection pipeline on a PIL image.

        Returns
        -------
        annotated_pil : PIL Image with boxes drawn
        alert_message : str to display in Gradio UI
        """
        if pil_image is None:
            return None, "⚠️  No image provided. Please upload or capture one."

        image_rgb = np.array(pil_image.convert("RGB"))

        # Inference
        blob, orig_w, orig_h = self.preprocess(image_rgb)
        outputs = self.session.run(self.output_names, {self.input_name: blob})

        boxes, scores, class_ids = self.postprocess(outputs, orig_w, orig_h)

        # Convert to BGR for OpenCV drawing
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if boxes:
            image_bgr      = self.draw_detections(image_bgr, boxes, scores, class_ids)
            detected_names = [CLASS_NAMES[cid] for cid in class_ids]
            alert_msg      = save_alert(image_bgr, detected_names)
        else:
            alert_msg = (
                "✅  No animal detected.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Farm field appears clear.\n"
                "No alert was generated."
            )

        # Convert back to PIL RGB for Gradio
        result_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result_pil = Image.fromarray(result_rgb)

        return result_pil, alert_msg


# ─────────────────────────────────────────────
# Module-level singleton (loaded once at startup)
# ─────────────────────────────────────────────
detector = FarmShieldONNX()


def predict_image(image) -> tuple[Image.Image | None, str]:
    """Gradio-facing wrapper around FarmShieldONNX.predict."""
    return detector.predict(image)