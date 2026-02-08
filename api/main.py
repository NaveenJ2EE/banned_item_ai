from fastapi import FastAPI, UploadFile
import shutil
from src.predict import predict

app = FastAPI()

@app.post("/check")
async def check(file: UploadFile):
    with open("temp.jpg", "wb") as f:
        shutil.copyfileobj(file.file, f)

    label, conf, text = predict("temp.jpg")
    return {
        "label": label,
        "confidence": conf,
        "ocr_text": text
    }