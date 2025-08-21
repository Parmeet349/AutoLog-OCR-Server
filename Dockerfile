# Base Python image
FROM python:3.11-slim

# Install system dependencies including Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose port for Render
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
