from ultralytics import YOLO
from PIL import Image
import io

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

    # Menentukan prediksi berdasarkan hasil deteksi
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = category_mapping.get(labels[class_id], "Tidak diketahui")
            predictions[label] = max(predictions[label], conf)

    total = sum(predictions.values())

    # Jika total prediksi 0, maka kembalikan nilai 0 untuk semua kategori
    if total == 0:
        return {label: 0 for label in predictions}

    # Menormalisasi prediksi untuk setiap kategori sehingga totalnya 100%
    normalized_predictions = {
        label: round((conf / total) * 100, 2) for label, conf in predictions.items()
    }

    return normalized_predictions
