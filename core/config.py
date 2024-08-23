import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent
SQLITE_URL = "sqlite+aiosqlite:///"

load_dotenv()


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_name: str = os.getenv("DB_FILENAME", "db.sqlite3")
    db_path: str = os.path.join(BASE_DIR, db_name)
    db_url: str = f"{SQLITE_URL}{db_path}"
    db_echo: bool = bool(int(os.getenv("DB_ECHO", 0)))
    secret_key: str | None = os.getenv("SECRET_KEY")


settings = Setting()
