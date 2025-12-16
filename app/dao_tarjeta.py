from sqlalchemy.orm import Session
import models, schemas


def get_card(db: Session, categoryId: int, tarjeta_id: int):
    return db.query(models.Tarjeta).filter(models.Tarjeta.id == tarjeta_id).filter(models.Tarjeta.idCategoria == categoryId).first()


def get_cards_by_deck(db: Session, idCategoria: int, userId: int):
    return db.query(models.Tarjeta).filter(models.Tarjeta.idCategoria == idCategoria).filter(models.Tarjeta.userId == userId).all()


def create_card(db: Session, tarjeta: schemas.TarjetaCreate, idCategoria:int, userId: int):
    db_card = models.Tarjeta(
        concepto = tarjeta.concepto,
        definicion = tarjeta.definicion,
        definicionExtra = tarjeta.definicionExtra,
        imagen = tarjeta.imagen,
        userId = userId,
        idCategoria = idCategoria
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, tarjeta_id: int, tarjeta_update: schemas.TarjetaUpdate):
    db_card = get_card(db, tarjeta_id)
    if not db_card:
        return None

    update_data = tarjeta_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_card, key, value)

    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, categoryId:int, tarjeta_id: int):
    db_card = get_card(db, categoryId, tarjeta_id)
    if not db_card:
        return None

    db.delete(db_card)
    db.commit()
    return True
