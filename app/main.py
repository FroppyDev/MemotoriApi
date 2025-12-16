from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dao, models, schemas, dao_tarjeta, dao_deck
from app.database import SessionLocal, engine
import verify
from seed import seed_data
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware




models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- SEED AL INICIAR ----
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_data(db)
    db.close()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_database)):
    db_user = dao.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return dao.create_user(db, user)

@app.get("/users/", response_model= list[schemas.User])
def get_users(skip:int = 0, limit:int = 10, db:Session = Depends(get_database)):
    users = dao.get_users(db, skip, limit)
    return users 

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_database)):
    user_exist = dao.get_user_by_email(db, user.email)
    if not user_exist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not verify.verify_password(user.password, user_exist.hashed_password):
        raise HTTPException(status_code=401, detail="Cotrasena incorrecta")
    
    return {
        "message": "Login exitoso",
        "token": "token",
        "user": {
            "id": user_exist.id,
            "name": "juanito alcachofa",
            "email": user_exist.email
        }
    }

# ---------------------- DECKS ------------------------

@app.post("/decks/{id}", response_model=schemas.Categoria)
def create_deck(deck: schemas.CrearCategoria, id: int = 1, db: Session = Depends(get_database)):
    return dao_deck.create_deck(db, deck, userId= id)


@app.get("/decks/", response_model=list[schemas.Categoria])
def get_decks(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return db.query(models.Categoria).offset(skip).limit(limit).all()


@app.get("/decks/user/{userId}", response_model=list[schemas.Categoria])
def get_decks_by_user(userId: int, db: Session = Depends(get_database)):
    decks = dao_deck.get_decks_by_user(db, userId)
    return decks


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
def delete_deck(userId:int, deck_id: int, db: Session = Depends(get_database)):
    deleted = dao_deck.delete_deck(db, userId, deck_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Deck no encontrado")
    return {"message": "Deck eliminado correctamente"}

# ---------------------- CARDS ------------------------

@app.post("/cards/{idCategoria}/{userId}", response_model=schemas.Tarjeta)
def create_card(tarjeta: schemas.TarjetaCreate, idCategoria: int, userId: int, db: Session = Depends(get_database)):
    return dao_tarjeta.create_card(db, tarjeta, idCategoria, userId)


@app.get("/cards/{tarjeta_id}", response_model=schemas.Tarjeta)
def get_card(tarjeta_id: int, db: Session = Depends(get_database)):
    card = dao_tarjeta.get_card(db, tarjeta_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card


@app.get("/cards/deck/{categoryId}/{userId}", response_model=list[schemas.TarjetaBase])
def get_cards_by_deck(categoryId, userId: int, db: Session = Depends(get_database)):
    return dao_tarjeta.get_cards_by_deck(db, categoryId, userId)


@app.put("/cards/{tarjeta_id}", response_model=schemas.Tarjeta)
def update_card(tarjeta_id: int, tarjeta_data: schemas.TarjetaUpdate, db: Session = Depends(get_database)):
    updated = dao_tarjeta.update_card(db, tarjeta_id, tarjeta_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return updated


@app.delete("/cards/deck/{categoryId}/{tarjeta_id}")
def delete_card(categoryId:int, tarjeta_id: int, db: Session = Depends(get_database)):
    deleted = dao_tarjeta.delete_card(db, categoryId, tarjeta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return {"message": "Tarjeta eliminada correctamente"}

