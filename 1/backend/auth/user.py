from datetime import datetime

import httpx
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.fake_db import fake_db


def decode_and_validate_token(token: str) -> str:
    # тут валидация
    if not token.endswith("_safe!"):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return token


def ensure_user_in_db(
    user_id: int, access_token: str, full_name: str, email: str, expires_at: str
) -> None:
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


def get_user(user_id: int, access_token: str) -> dict:
    token = decode_and_validate_token(token=access_token)
    user = fake_db.get(user_id)

    if (
        user is None
        or user["expires_at"] <= datetime.utcnow().timestamp()
        or user["access_token"] != token
    ):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user


async def get_user_info_from_vk(access_token: str, user_id: int) -> dict:
    async with httpx.AsyncClient() as httpx_client:
        url = "https://api.vk.com/method/users.get"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-encoded",
        }
        params = {"v": "5.131", "user_id": user_id}
        resp = await httpx_client.get(
            url,
            headers=headers,
            params=params,
        )
        resp_json = resp.json()
    response_json = resp_json["response"][0]
    full_name = f"{response_json['first_name']} {response_json['last_name']}"

    return {"full_name": full_name}
