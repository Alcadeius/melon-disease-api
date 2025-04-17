FROM python:3.10-slim

# Install dependencies including libGL untuk OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

