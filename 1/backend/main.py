import uvicorn
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends

from auth.user import get_user, ensure_user_in_db, get_user_info_from_vk
from config import settings

app = FastAPI()

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vk_client = OAuth2(
    settings.VK_APP_ID,
    settings.VK_APP_SECRET,
    "https://oauth.vk.com/authorize",
    "https://oauth.vk.com/access_token",
)

oauth2_authorize_callback = OAuth2AuthorizeCallback(vk_client, redirect_url="http://localhost:5173/oauth-callback")


@app.get("/get_auth_url")
async def get_auth_url_route() -> dict:
    authorization_url = await vk_client.get_authorization_url(
        redirect_uri="http://localhost:5173/oauth-callback",
        scope=["email"],
    )
    return {"result": authorization_url}


@app.post("/oauth-callback", name="oauth-callback")
async def oauth_callback_route(access_token_state=Depends(oauth2_authorize_callback)) -> dict:
    data, _ = access_token_state
    access_token = data["access_token"]
    expires_at = data["expires_at"]
    user_id = data["user_id"]
    email = data["email"]

    safe_access_token = access_token + "_safe!"
    user_info = await get_user_info_from_vk(access_token=access_token, user_id=user_id)

    ensure_user_in_db(
        user_id=user_id,
        access_token=safe_access_token,
        full_name=user_info["full_name"],
        email=email,
        expires_at=expires_at,
    )

    return {"user_id": user_id, "access_token": safe_access_token}


@app.get("/get_me")
async def get_me_route(user=Depends(get_user)) -> dict:
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
