import hashlib

from loguru import logger

from core.config import settings


def get_password_hash(unhashed_password: str) -> str:
    iterations: int = 600000
    algorithm: str = hashlib.sha512().name
    if not isinstance(settings.secret_key, str) or not settings.secret_key:
        logger.error(
            f"SECRET_KEY variable is not defined."
            f"This function cant't work without this key!"
        )
        raise ValueError("SECRET_KEY variable is not defined.")
    hash = hashlib.pbkdf2_hmac(
        algorithm,
        unhashed_password.encode("utf-8"),
        settings.secret_key.encode("utf-8"),
        iterations,
    )
    return hash.hex()
