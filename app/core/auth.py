from  passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings
from schemas.schema import UserRole

ctx=CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme=HTTPBearer()


def password_hash(password:str)->str:
    HashedPass=ctx.hash(password)
    return HashedPass


def verify_password(plain_password:str, hashed_password:str)->bool:
    passwordVerify=ctx.verify(plain_password, hashed_password)
    return passwordVerify

def create_access_token(User_id:str, Username:str, role: UserRole)->str:

    expire=datetime.now(timezone.utc) + timedelta(minutes=15)

    payload={
        "sub": User_id,
        "username": Username,
        "role":role.value if isinstance(role, UserRole) else role,
        "exp":expire
    }

    token=jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token
