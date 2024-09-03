import datetime

import jwt

from core.config import settings


async def encode_jwt(
    payload: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_days: int | None = None,
    key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
) -> str:
    to_encode = payload.copy()
    now_time = datetime.datetime.now(datetime.UTC)
    expire_time = now_time + datetime.timedelta(minutes=expire_minutes)
    if expire_days:
        expire_time = now_time + datetime.timedelta(days=expire_days)
    to_encode.update(iat=now_time, exp=expire_time)
    encoded_data: str = jwt.encode(
        payload=to_encode, key=key, algorithm=algorithm
    )
    return encoded_data


async def decode_jwt(
    token: str | bytes,
    key: str = settings.auth.public_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
) -> dict:
    decoded_data: dict = jwt.decode(jwt=token, key=key, algorithms=[algorithm])
    return decoded_data
