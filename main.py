from fastapi import FastAPI, Depends, HTTPException, status
from schemes import *
from database import *
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

app = FastAPI(
    title="Auth Service API",
    description="Сервис авторизации",
    version="1.0.0"
)

@app.post("/register", response_model=UserResponse)
async def register(user: CreateUser, db: Depends(get_db)):
    pass