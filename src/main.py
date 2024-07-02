from fastapi import FastAPI 
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.settings import DATABASE_URL
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re 
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator



##################################
# БЛОК ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ #
##################################


# Фабрика сессий с базой данных
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



#################################
# БЛОК ДЛЯ РАБОТЫ С МОДЕЛЯМИ БД #
#################################


Base = declarative_base()

class User(Base): 
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean(), default=True)



########################################
# БЛОК ДЛЯ РАБОТЫ С БД БИЗНЕС-КОНТЕКСТ #
########################################

# По сути работа класса UserDAL с сессией БД
class UserDAL: 
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, name: str, surname: str, email: str
    ) -> User: 
        new_user = User(
            name = name,
            surname = surname,
            email = email,  
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    
##################################
# БЛОК ДЛЯ РАБОТЫ С API МОДЕЛЯМИ #
##################################


LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")

class TunedModel(BaseModel): 
    class Config: 
        """говорит pydantic конвертировать не только dict в json"""
        orm_mode = True
        """json-фицирует всё что входит в этот класс"""

class ShowUser(TunedModel): 
    user_id: uuid.UUID
    name: str 
    surname: str
    email: EmailStr
    is_active: bool 

class UserCreate(BaseModel): 
    name: str
    surname: str
    email: EmailStr

    @field_validator("name")
    def validate_name(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value): 
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value 
    
    @field_validator("surname")
    def validate_surname(cls, value): 
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException ( 
                status_code=422, detail="Surname should contain only letters"
            )
        return value



#####################
# БЛОК С API ROUTES #
#####################

app = FastAPI(
    title = "Some Landing"
)

user_router = APIRouter()

async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session: 
        async with session.begin(): 
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name = body.name,
                surname = body.surname,
                email = body.email,
            )
            return ShowUser(
                user_id = user.user_id,
                name = user.name, 
                surname = user.surname, 
                email = user.email, 
                is_active = user.is_active
            )
    

@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser: 
    return await _create_new_user(body)

# Создание инстанса для всех роутев (роутер, который собирает в себя остальные роутеры)
main_api_router = APIRouter()

# Подключение всех "младших роутеров" к основному роутеру
main_api_router.include_router(
    user_router, 
    prefix="/user", 
    tags=["user"]
)
# Включение главного роутера в app
app.include_router(main_api_router)

if __name__ == "__main__": 
    uvicorn.run(app, host="localhost", port=8000)