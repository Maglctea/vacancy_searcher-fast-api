"""
Config file
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

# Dirs
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# DB
DB_DRIVER = os.getenv("POSTGRES_DRIVER", "postgresql+asyncpg")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_NAME = os.getenv("POSTGRES_DB", "ja_bot")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

POSTGRES_URL = URL.create(
    drivername=DB_DRIVER,
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

EMAIL_REG_EXP = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

NAME_REG_EXP = r"^[A-Za-zА-ЯЁа-яё]+$"