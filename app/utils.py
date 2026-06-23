import cv2
import numpy as np
from app.config import CLASS_NAMES

CLASS_COLORS = {
    "Bear": (255, 0, 0),
    "Boar": (0, 255, 0),
    "Elephant": (0, 0, 255),
}

def compute_iou(box, boxes):
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])

    inter_area = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])

    union = box_area + boxes_area - inter_area + 1e-6
    return inter_area / union

def non_max_suppression(boxes, scores, iou_threshold=0.45):
    if len(boxes) == 0:
        return []

    indices = np.argsort(scores)[::-1]
    keep = []

    while len(indices) > 0:
        current = indices[0]
        keep.append(current)

        if len(indices) == 1:
            break

        remaining = indices[1:]
        ious = compute_iou(boxes[current], boxes[remaining])
        indices = remaining[ious < iou_threshold]

    return keep

def draw_detections(image_bgr, boxes, scores, class_ids):
    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = map(int, box)
        class_name = CLASS_NAMES[int(class_id)]
        color = CLASS_COLORS.get(class_name, (0, 255, 255))

        label = f"{class_name}: {score:.2f}"

        cv2.rectangle(image_bgr, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            image_bgr,
            label,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return image_bgr