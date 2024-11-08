import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

LOGLEVEL: str = os.getenv("LOGLEVEL", "DEBUG")
LOGFILE: str = os.getenv("LOGFILE", "main.log")
ERROR_LOGFILE: str = os.getenv("ERROR_LOGFILE", "error.log")

logger.add(LOGFILE, level=LOGLEVEL, rotation="5 MB")
logger.add(ERROR_LOGFILE, level="ERROR", rotation="1 MB")


class SQLiteDBSettings(BaseModel):
    _db_path: str = os.path.join(
        BASE_DIR, os.getenv("DB_FILENAME", "db.sqlite3")
    )

    url: str = f"sqlite+aiosqlite:///{_db_path}"
    echo: bool = bool(int(os.getenv("DB_ECHO", 0)))


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / ".secrets" / "private.pem"
    public_key_path: Path = BASE_DIR / ".secrets" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    )
    refresh_token_expire_days: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "1")
    )


class Settings(BaseSettings):
    api_v1_prefix: str
    db: SQLiteDBSettings = SQLiteDBSettings()
    auth: AuthJWT = AuthJWT()


settings = Settings(
    api_v1_prefix="/api/v1",
)

if os.environ["DB_TYPE"] == "sqlite":
    settings.db = SQLiteDBSettings()
