FROM python:3.11-slim

# Avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, including Tesseract OCR.
# Replaced the obsolete legacy package libgl1-mesa-glx with libgl1 (modern Debian Bookworm OpenGL library).
# Uses a POSIX shell compliant retry loop to handle transient builder network failures.
RUN apt-get clean && \
    for i in 1 2 3; do apt-get update && break || sleep 5; done && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy requirements first to leverage Docker build cache
COPY backend/ocr/requirements.txt /workspace/backend/ocr/requirements.txt
RUN pip install --no-cache-dir -r /workspace/backend/ocr/requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy entire directory structure into the workspace
COPY backend/ /workspace/backend/
COPY frontend/ /workspace/frontend/

WORKDIR /workspace/backend/ocr

# Expose Flask port
EXPOSE 5000

# Start Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
