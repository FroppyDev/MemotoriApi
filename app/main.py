from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app import dao, models, schemas, dao_tarjeta, dao_deck, verify
from app.database import SessionLocal, engine
from app.seed import seed_data
from datetime import datetime
from app.uploads import router as upload_router


# -------------------- APP --------------------

app = FastAPI()

# -------------------- IMÁGENES --------------------

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "imagenes"
IMAGES_DIR.mkdir(exist_ok=True)

app.mount("/imagenes", StaticFiles(directory=IMAGES_DIR), name="imagenes")

app.include_router(upload_router)


# -------------------- DB --------------------

models.Base.metadata.create_all(bind=engine)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://memotoriapi.onrender.com",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- SEED --------------------

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_data(db)
    db.close()

# -------------------- USERS --------------------

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_database)):
    db_user = dao.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return dao.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_database)):
    return dao.get_users(db, skip, limit)

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_database)):
    user_exist = dao.get_user_by_email(db, user.email)
    if not user_exist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify.verify_password(user.password, user_exist.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "message": "Login exitoso",
        "token": "token",
        "user": {
            "id": user_exist.id,
            "email": user_exist.email
        }
    }

# -------------------- DECKS --------------------

@app.post("/decks/{id}", response_model=schemas.Categoria)
def create_deck(deck: schemas.CrearCategoria, id: int = 1, db: Session = Depends(get_database)):
    return dao_deck.create_deck(db, deck, userId=id)

@app.get("/decks/", response_model=list[schemas.Categoria])
def get_decks(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

@app.get("/decks/user/{userId}", response_model=list[schemas.Categoria])
def get_decks_by_user(userId: int, db: Session = Depends(get_database)):
    return dao_deck.get_decks_by_user(db, userId)

@app.get("/decks/{deck_id}", response_model=schemas.Categoria)
def get_deck(deck_id: int, db: Session = Depends(get_database)):
    deck = dao_deck.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck no encontrado")
    return deck

@app.put("/decks/{deck_id}", response_model=schemas.Categoria)
def update_deck(deck_id: int, deck_data: schemas.ActualizarCategoria, db: Session = Depends(get_database)):
    updated = dao_deck.update_deck(db, deck_id, deck_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Deck no encontrado")
    return updated

@app.delete("/decks/{userId}/{deck_id}")
def delete_deck(userId: int, deck_id: int, db: Session = Depends(get_database)):
    if not dao_deck.delete_deck(db, userId, deck_id):
        raise HTTPException(status_code=404, detail="Deck no encontrado")
    return {"message": "Deck eliminado correctamente"}

# -------------------- CARDS --------------------

@app.post("/cards/{idCategoria}/{userId}", response_model=schemas.Tarjeta)
def create_card(tarjeta: schemas.TarjetaCreate, idCategoria: int, userId: int, db: Session = Depends(get_database)):
    return dao_tarjeta.create_card(db, tarjeta, idCategoria, userId)

@app.get("/sync/cards/{userId}")
def sync_cards(
    userId: int,
    since: datetime,
    db: Session = Depends(get_database)
):
    return (
        db.query(models.Tarjeta)
        .filter(models.Tarjeta.userId == userId)
        .filter(models.Tarjeta.updated_at > since)
        .all()
    )

@app.get("/sync/decks/{userId}")
def sync_decks(
    userId: int,
    since: datetime,
    db: Session = Depends(get_database)
):
    return (
        db.query(models.Categoria)
        .filter(models.Categoria.userId == userId)
        .filter(models.Categoria.updated_at > since)
        .all()
    )

@app.get("/cards/{tarjeta_id}", response_model=schemas.Tarjeta)
def get_card(tarjeta_id: int, db: Session = Depends(get_database)):
    card = dao_tarjeta.get_card(db, tarjeta_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card

@app.get("/cards/deck/{categoryId}/{userId}", response_model=list[schemas.TarjetaBase])
def get_cards_by_deck(categoryId: int, userId: int, db: Session = Depends(get_database)):
    return dao_tarjeta.get_cards_by_deck(db, categoryId, userId)

@app.put("/cards/{tarjeta_id}", response_model=schemas.Tarjeta)
def update_card(tarjeta_id: int, tarjeta_data: schemas.TarjetaUpdate, db: Session = Depends(get_database)):
    updated = dao_tarjeta.update_card(db, tarjeta_id, tarjeta_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return updated

@app.delete("/cards/deck/{categoryId}/{tarjeta_id}")
def delete_card(categoryId: int, tarjeta_id: int, db: Session = Depends(get_database)):
    if not dao_tarjeta.delete_card(db, categoryId, tarjeta_id):
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return {"message": "Tarjeta eliminada correctamente"}
