from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return passwd_context.verify(plain_password, hashed_password)