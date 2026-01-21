from fastapi import FastAPI, UploadFile, File
import uvicorn
from uvr import models
from uvr.utils.get_models import download_all_models
import os
import tempfile

app = FastAPI()

# download models once on startup
@app.on_event("startup")
def load_models():
    # if this fails you may need to set up model files manually
    models_json = download_all_models({})
    download_all_models(models_json)

@app.post("/separate")
async def separate_file(file: UploadFile = File(...)):
    # save uploaded audio
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    contents = await file.read()
    tmp.write(contents)
    tmp.close()

    demucs = models.Demucs(name="hdemucs_mmi", other_metadata={"segment":2, "split":True}, device="cpu", logger=None)
    result = demucs(tmp.name)

    # results is dict with {"separated": {"vocals": ..., "other": ..., ...}}
    vocals_path = result["separated"]["vocals"]
    return {"vocals_file": vocals_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
