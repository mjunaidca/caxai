from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DB_URL = config("DB_URL", cast=Secret)
TEST_DB_URL = config("TEST_DB_URL", cast=Secret)
AUTH_SERVER_URL = config("AUTH_SERVER_URL", cast=str)