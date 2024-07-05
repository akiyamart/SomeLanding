from envparse import Env
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL", 
    default = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL", 
    default = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
)