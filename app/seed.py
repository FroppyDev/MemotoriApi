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
    return f"https://memotoriapi.onrender.com/imagenes/{filename}"


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
    categoria_prog = models.Categoria(
        nombre="Programación",
        descripcion="Conceptos básicos de programación orientada a objetos",
        userId=user.id,
        imagen=copy_default_image("gato.png")
    )

    db.add(categoria_prog)
    db.commit()
    db.refresh(categoria_prog)

    # Tarjetas
    cards_prog = [
    models.Tarjeta(
        concepto="¿Qué es la Programación Orientada a Objetos?",
        definicion="Un paradigma de programación basado en objetos.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Usa clases y objetos para organizar el código."
    ),
    models.Tarjeta(
        concepto="¿Qué es una clase?",
        definicion="Una plantilla para crear objetos.",
        definicionExtra="Una clase Persona define nombre y edad.",
        userId=user.id,
        idCategoria=categoria_prog.id
    ),
    models.Tarjeta(
        concepto="¿Qué es un objeto?",
        definicion="Una instancia de una clase.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="persona1 es un objeto de la clase Persona."
    ),
    models.Tarjeta(
        concepto="¿Qué es la herencia?",
        definicion="Permite que una clase herede atributos y métodos de otra.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="La clase Estudiante hereda de Persona."
    ),
    models.Tarjeta(
        concepto="¿Qué es el encapsulamiento?",
        definicion="Oculta los detalles internos de un objeto.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Usar atributos privados y getters/setters."
    ),
    models.Tarjeta(
        concepto="¿Qué es el polimorfismo?",
        definicion="Permite usar el mismo método de diferentes formas.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Un método que se comporta distinto según la clase."
    ),
    models.Tarjeta(
        concepto="¿Qué es una interfaz?",
        definicion="Define métodos que una clase debe implementar.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Garantiza un comportamiento común entre clases."
    ),
    models.Tarjeta(
        concepto="¿Qué es una abstracción?",
        definicion="Representa solo los aspectos esenciales de un objeto.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Una clase abstracta Vehículo."
    ),
    models.Tarjeta(
        concepto="¿Qué es un constructor?",
        definicion="Un método que se ejecuta al crear un objeto.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="Inicializa los valores del objeto."
    ),
    models.Tarjeta(
        concepto="¿Qué es un método?",
        definicion="Una función definida dentro de una clase.",
        userId=user.id,
        idCategoria=categoria_prog.id,
        definicionExtra="calcularEdad() dentro de Persona."
    )]

    db.add_all(cards_prog)
    db.commit()

    categoria_ingles = models.Categoria(
        nombre="Inglés Básico",
        descripcion="Vocabulario básico de inglés con ejemplos",
        userId=user.id,
        imagen=copy_default_image("gato.png")
    )

    db.add(categoria_ingles)
    db.commit()
    db.refresh(categoria_ingles)

    cards_ingles = [
        models.Tarjeta(
            concepto="Apple",
            definicion="Manzana",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="I eat an apple every day."
        ),
        models.Tarjeta(
            concepto="Book",
            definicion="Libro",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="She is reading a book."
        ),
        models.Tarjeta(
            concepto="House",
            definicion="Casa",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="My house is very small."
        ),
        models.Tarjeta(
            concepto="Car",
            definicion="Auto",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="He drives a car."
        ),
        models.Tarjeta(
            concepto="Dog",
            definicion="Perro",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="The dog is friendly."
        ),
        models.Tarjeta(
            concepto="Water",
            definicion="Agua",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="I drink water."
        ),
        models.Tarjeta(
            concepto="Food",
            definicion="Comida",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="This food is delicious."
        ),
        models.Tarjeta(
            concepto="Friend",
            definicion="Amigo",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="He is my best friend."
        ),
        models.Tarjeta(
            concepto="School",
            definicion="Escuela",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="I go to school every day."
        ),
        models.Tarjeta(
            concepto="Music",
            definicion="Música",
            userId=user.id,
            idCategoria=categoria_ingles.id,
            definicionExtra="I love listening to music."
        ),
    ]

    db.add_all(cards_ingles)
    db.commit()


    print("Datos iniciales insertados correctamente.")
