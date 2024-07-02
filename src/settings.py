from envparse import Env
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL", 
    default = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)