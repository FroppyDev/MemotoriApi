import uuid
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

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    filepath = IMAGES_DIR / filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"https://memotoriapi.onrender.com/imagenes/tarjetas/{filename}"
    }
