# seed.py
from sqlalchemy.orm import Session
import models
import os
import shutil

def copy_default_image(src_file: str, dest_folder: str) -> str:
    """
    Copia una imagen desde /default_assets hacia /uploads
    Retorna la URL accesible.
    """

    # Asegurar carpeta destino
    os.makedirs(dest_folder, exist_ok=True)

    filename = os.path.basename(src_file)
    dest_path = os.path.join(dest_folder, filename)

    # Copiar archivo
    shutil.copy(src_file, dest_path)

    # Crear URL pública
    folder_name = dest_folder.replace("imagenes/", "")
    return f"/imagenes/{folder_name}/{filename}"

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
        imagen=copy_default_image(
            "imagenes/default/default.jpg",
            "imagenes/categorias"
        )
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
        imagen=copy_default_image(
            "imagenes/default/python.png",
            "imagenes/tarjetas"
        )
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
