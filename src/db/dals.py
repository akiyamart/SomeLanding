from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from sqlalchemy import update, and_, select
from uuid import UUID
from src.db.models import User 
class UserDAL: 
    def __init__(self, db_session: AsyncSession): 
        self.db_session = db_session
    
    async def create_user(
            self, name: str, surname: str, email: str
    ) -> User: 
        new_user = User(
            name=name, 
            surname=surname, 
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    
    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User). \
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(is_active=False). \
            returning(User.user_id)
        result = await self.db_session.execute(query)
        deleted_user_id = result.fetchone()
        if deleted_user_id is not None: 
            return deleted_user_id[0]

    async def update_user(self, **kwargs) -> Union[UUID, None]:
        query = update(User). \
            where(User.is_active == True). \
            values(kwargs). \
            returning(User.user_id)
        