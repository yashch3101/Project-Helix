from datetime import datetime, timedelta, timezone
from app.core.config import settings

import jwt
from pwdlib import PasswordHash
import traceback

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    try:
        print("HASH START")
        hashed = password_hash.hash(password)
        print("HASH DONE")
        return hashed

    except Exception as e:
        traceback.print_exc()
        print("HASH ERROR:", repr(e))
        raise


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )