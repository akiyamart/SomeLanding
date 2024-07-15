
from uuid import UUID
from fastapi import APIRouter
from typing import Union
from src.api.models import UserCreate, ShowUser
from src.db.dals import UserDAL, PortalRole
from src.api.handlers.auth.hasher import Hasher


user_router = APIRouter()

async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin(): 
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name = body.name,
            surname = body.surname,
            email = body.email,
            hashed_password = Hasher.get_password_hash(body.password),
            roles = [PortalRole.ROLE_PORTAL_USER, ]
        )
        return ShowUser(
            user_id = user.user_id,
            name = user.name, 
            surname = user.surname, 
            email = user.email, 
            is_active = user.is_active,
        )
    
async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin(): 
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id

async def _get_user_by_id(user_id, session) -> Union[ShowUser, None]: 
    async with session.begin(): 
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None: 
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active 
            )
            
async def _update_user(updated_user_params: dict, user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin(): 
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id,
            **updated_user_params)
        return updated_user_id


