from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from loguru import logger

password_hasher = PasswordHasher()


def get_password_hash(unhashed_password: str) -> str:
    return password_hasher.hash(unhashed_password)


def password_validation(password: str, hash: str) -> bool:
    try:
        password_hasher.verify(hash=hash, password=password)
    except VerifyMismatchError:
        return False
    except VerificationError as exception_trace:
        logger.error(
            f"Verification fails for other reasons. {exception_trace}"
        )
    return True
