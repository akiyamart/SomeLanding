from typing import Union, Optional
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException 
from src.db.dals import UserDAL
from src.api.handlers.auth.hasher import Hasher
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

login_router = APIRouter()

async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email,
        )

async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await _get_user_by_email_for_auth(email, db)
    if user is None: 
        return 
    if not Hasher.verify_password(password, user.hashed_password): 
        return 
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now() + expires_delta
    else: expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

