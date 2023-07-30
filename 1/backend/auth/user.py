from datetime import datetime

from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.fake_db import fake_db


def ensure_user_in_db(access_token: str, name: str, expires_at: str) -> None:
    if fake_db.get(access_token) is not None:
        return
    fake_db[access_token] = {"name": name, "expires_at": expires_at}


def get_user(token: str):
    user = fake_db.get(token)

    if user is None or user["expires_at"] <= datetime.utcnow().timestamp():
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return user
