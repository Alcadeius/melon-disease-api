from ultralytics import YOLO
from PIL import Image
import io
import os

model_path = "models/best.pt"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")
model = YOLO("models/best.pt")


def predict_image(file_bytes: bytes):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    results = model(image)

    labels = ["anthracnose", "downy mildew", "leaf"]
    category_mapping = {
        "leaf": "Sehat",
        "anthracnose": "Sakit - Anthracnose",
        "downy mildew": "Sakit - Downy Mildew",
    }

    predictions = {v: 0 for v in category_mapping.values()}

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = category_mapping.get(labels[class_id], "Tidak diketahui")
            predictions[label] = max(predictions[label], conf)

    total = sum(predictions.values())

    if total == 0:
        return {label: 0 for label in predictions}

    normalized_predictions = {
        label: round((conf / total) * 100, 2) for label, conf in predictions.items()
    }

    return normalized_predictions
