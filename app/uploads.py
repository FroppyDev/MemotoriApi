import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Solo imágenes válidas
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Formato no soportado")

    # Nombre único
    filename = file.filename.replace(" ", "_")
    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"https://memotoriapi.onrender.com/imagenes/{filename}"

    return {"file_url": file_url}
