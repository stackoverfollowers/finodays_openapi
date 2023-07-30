from datetime import datetime

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.fake_db import fake_db


def decode_and_validate_token(token: str) -> str:
    # тут валидация
    if not token.endswith("_safe!"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return token


def ensure_user_in_db(user_id: int, access_token: str, full_name: str, email: str, expires_at: str) -> None:
    if (user := fake_db.get(user_id)) is not None:
        if user["access_token"] != access_token:
            user["access_token"] = access_token
            user["expires_at"] = expires_at
        return
    fake_db[user_id] = {
        "access_token": access_token,
        "email": email,
        "full_name": full_name,
        "expires_at": expires_at,
    }


def get_user(user_id: int, access_token: str):
    token = decode_and_validate_token(token=access_token)
    user = fake_db.get(user_id)

    if (
        user is None
        or user["expires_at"] <= datetime.utcnow().timestamp()
        or user["access_token"] != token
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return user
