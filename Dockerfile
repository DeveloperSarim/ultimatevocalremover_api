# Start from an image that already has torch + torchaudio preinstalled
FROM pytorch/pytorch:2.0.1-cuda11.8-cudnn8-runtime

WORKDIR /app

# Copy only requirements first to speed up build caching
COPY requirements.txt .

# Install only fastapi + uvicorn + project deps
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
