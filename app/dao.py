from sqlalchemy.orm import Session 
from fastapi import HTTPException
from app import models, schemas 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_users(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    fake_hashed_pass = user.password + "fakehash"
    db_user = models.User(email= user.email, hashed_password= fake_hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user