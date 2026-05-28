FROM python:3.11-slim

# Install system dependencies, including Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY backend/ocr/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the backend source code
COPY backend/ocr/ .

# Ensure frontend files are in the expected relative path
# The backend expects static files at ../../frontend relative to this file
COPY frontend/ /frontend/
# We can create a symlink or adjust the search path.
# Since app.py looks for:
# frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
# Within the Docker container, we can structure the app to match this layout:
# Workdir /app/backend/ocr/ and copy source code there.
# Let's restructure the Docker copying for seamless relative path resolution.

WORKDIR /workspace

# Copy entire directory structure into the workspace
COPY backend/ /workspace/backend/
COPY frontend/ /workspace/frontend/

WORKDIR /workspace/backend/ocr

# Expose Flask port
EXPOSE 5000

# Start Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
