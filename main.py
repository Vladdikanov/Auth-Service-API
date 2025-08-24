from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemes import *
from database import *
from auth import *
import models
import crud
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service API",
    description="Сервис авторизации",
    version="1.0.0"
)

@app.post("/register", response_model=UserResponse)
async def register(user: CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегестрирован")
    return crud.create_user(db, user.username, user.password)

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data)
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Не верный токен")
    user = crud.get_user_by_username(db, username)
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)