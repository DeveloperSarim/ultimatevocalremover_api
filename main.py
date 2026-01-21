from fastapi import FastAPI, UploadFile, File
import uvicorn
from uvr import models
from uvr.utils.get_models import download_all_models
import torch
import tempfile
import os

app = FastAPI()

# Download models on first startup
@app.on_event("startup")
def load_models():
    models_json = download_all_models({})
    download_all_models(models_json)

@app.post("/separate")
async def separate_audio(file: UploadFile = File(...)):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_file.write(await file.read())
    tmp_file.close()

    demucs = models.Demucs(name="hdemucs_mmi", other_metadata={"segment":2,"split":True}, device="cpu", logger=None)
    res = demucs(tmp_file.name)

    vocals = res["separated"]["vocals"]
    return {"vocals_path": vocals}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
