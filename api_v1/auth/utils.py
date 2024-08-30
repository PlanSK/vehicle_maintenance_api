import datetime
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from loguru import logger

from core.config import settings

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


def encode_jwt(
    payload: dict,
    key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes
) -> str:
    to_encode = payload.copy()
    now_time = datetime.datetime.now(datetime.UTC)
    expire_time = now_time + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(iat=now_time, exp=expire_time)
    encoded_data: str = jwt.encode(
        payload=to_encode, key=key, algorithm=algorithm
    )
    return encoded_data


def decode_jwt(
    token: str | bytes,
    key: str = settings.auth.public_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    decoded_data = jwt.decode(jwt=token, key=key, algorithms=[algorithm])
    return decoded_data
