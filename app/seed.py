# seed.py
from sqlalchemy.orm import Session
from app import models
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "imagenes"
DEFAULT_DIR = IMAGES_DIR / "default"
DEFAULT_IMAGE = DEFAULT_DIR / "default.jpg"


def copy_default_image(filename: str) -> str:
    """
    Copia la imagen por defecto a app/imagenes/{filename}
    y devuelve la ruta pública.
    """
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_DIR.mkdir(parents=True, exist_ok=True)

    dest_path = IMAGES_DIR / filename

    if not dest_path.exists():
        shutil.copy(DEFAULT_IMAGE, dest_path)

    # Esta ruta es la que usará FastAPI para servir la imagen
    return f"/imagenes/{filename}"


def seed_data(db: Session):
    existing_user = db.query(models.User).first()
    if existing_user:
        print("Seed data ya existe. No se insertará nada.")
        return

    print("Insertando datos iniciales...")

    # Usuario
    user = models.User(
        email="admin@example.com",
        hashed_password="admin123fakehash"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Categoría
    categoria = models.Categoria(
        nombre="Básico",
        descripcion="Categoría inicial",
        userId=user.id,
        imagen=copy_default_image("default_categoria.jpg")
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    # Tarjetas
    card1 = models.Tarjeta(
        concepto="¿Qué es Python?",
        definicion="Un lenguaje de programación.",
        userId=user.id,
        idCategoria=categoria.id,
        imagen=copy_default_image("python.jpg")
    )

    card2 = models.Tarjeta(
        concepto="¿Qué es una API?",
        definicion="Una interfaz para comunicarse entre sistemas.",
        userId=user.id,
        idCategoria=categoria.id
    )

    db.add_all([card1, card2])
    db.commit()

    print("Datos iniciales insertados correctamente.")
