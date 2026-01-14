from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.auth import authenticate_user, create_access_token
from app.schemas import UserCreate

@app.post("/auth/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(user.email, user.password, db)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

from app.auth import get_current_user
from app.models import User

@app.get("/profile")
def profile(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}

@app.get("/")
def root():
    return {"message": "Я жив! Ахахахахахахахах!!! Мяу!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Eclipser",
        "level": 1
    }

@app.post("/echo")
def echo(data: dict):
    return data