from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException 
from src.db.dals import UserDAL
from src.api.handlers.auth.hasher import Hasher

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
