# Use a valid PyTorch base image
FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime

WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install FastAPI, Uvicorn, and dependencies
RUN pip install fastapi uvicorn python-multipart

# Install your project as package (so internal imports work)
RUN pip install .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
