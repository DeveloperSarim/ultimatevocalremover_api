# 🧠 Use official PyTorch image (has torch + torchaudio)
FROM pytorch/pytorch:2.0.1-cuda11.8-cudnn8-runtime

# 📌 Set working directory
WORKDIR /app

# 🔁 Copy all your code
COPY . .

# ⬆ Upgrade pip
RUN pip install --upgrade pip

# 📦 Install FastAPI + Uvicorn
RUN pip install fastapi uvicorn python-multipart

# 📦 Install this project as a Python package
RUN pip install .

# 🧪 Expose the port
EXPOSE 8000

# 🚀 Serve the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
