# Gunakan image dasar yang kecil
FROM python:3.10-slim

# Install hanya dependensi sistem yang dibutuhkan
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set workdir ke folder app
WORKDIR /app

# Salin file requirements dulu agar caching efisien
COPY requirements.txt .

# Install dependencies Python tanpa cache
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek
COPY . .

# Jalankan uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
