from sqlalchemy.orm import Session
from app import models, schemas


def get_deck(db: Session, userId:int, idCategoria: int):
    return db.query(models.Categoria).filter(models.Categoria.id == idCategoria).filter(models.Categoria.userId == userId).first()


def get_decks_by_user(db: Session, userId: int):
    return db.query(models.Categoria).filter(models.Categoria.userId == userId).all()


def get_decks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def create_deck(db: Session, categoria: schemas.CrearCategoria, userId: int):
    db_deck = models.Categoria(
        nombre = categoria.nombre,
        userId = userId,
        descripcion = categoria.descripcion,
        imagen = categoria.imagen,
        color = categoria.color,
        smart = categoria.smart,
        latitud = categoria.latitud,
        longitud = categoria.longitud,
        radioMetros = categoria.radioMetros
    )

    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def update_deck(db: Session, idCategoria: int, deck_update: schemas.ActualizarCategoria):
    db_deck = get_deck(db, idCategoria)
    if not db_deck:
        return None

    update_data = deck_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deck, key, value)

    db.commit()
    db.refresh(db_deck)
    return db_deck


def delete_deck(db: Session, userId:int, idCategoria: int):
    db_deck = get_deck(db, userId, idCategoria)
    if not db_deck:
        return None

    db.delete(db_deck)
    db.commit()
    return True
