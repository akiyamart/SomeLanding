from fastapi import FastAPI 
import uvicorn
from fastapi.routing import APIRouter

from src.api.main_handlers import user_router
from src.api.main_handlers import login_router

app = FastAPI(
    title = "Some Landing"
)


# Создание инстанса для всех роутев (роутер, который собирает в себя остальные роутеры)
main_api_router = APIRouter()

# Подключение всех "младших роутеров" к основному роутеру
main_api_router.include_router(
    user_router, 
    prefix="/user", 
    tags=["user"]
)
main_api_router.include_router(
    login_router, 
    prefix="/login", 
    tags=["login"]
)
# Включение главного роутера в app
app.include_router(main_api_router)

if __name__ == "__main__": 
    uvicorn.run(app, host="localhost", port=8000)