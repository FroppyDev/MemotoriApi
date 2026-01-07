import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "imagenes" / "tarjetas"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):

    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Formato no soportado")

    filename = file.filename.replace(" ", "_")
    filepath = IMAGES_DIR / filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"https://memotoriapi.onrender.com/imagenes/{filename}"

    return {
        "url": file_url
    }
