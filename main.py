from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemes import *
from database import *
import models
import crud
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Auth Service API",
    description="Сервис авторизации",
    version="1.0.0"
)

@app.post("/register", response_model=UserResponse)
async def register(user: CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегестрирован")
    return crud.create_user(db, user.email, user.password)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)