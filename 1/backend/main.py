import httpx
import uvicorn
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends

from auth.user import get_user, ensure_user_in_db
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

oauth2_authorize_callback = OAuth2AuthorizeCallback(vk_client, "oauth-callback")


@app.get("/get_auth_url")
async def home():
    authorization_url = await vk_client.get_authorization_url(
        "http://localhost:8000/oauth-callback", scope=["email"],
    )
    return {'result': authorization_url}


@app.get("/oauth-callback", name="oauth-callback")
async def oauth_callback(access_token_state=Depends(oauth2_authorize_callback)):
    data, _ = access_token_state
    print(data)
    access_token = data["access_token"]
    expires_at = data["expires_at"]
    user_id = data["user_id"]
    email = data["email"]

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
    print(resp_json)
    response_json = resp_json["response"][0]

    safe_access_token = access_token + "_safe!"
    full_name = f"{response_json['first_name']} {response_json['last_name']}"

    ensure_user_in_db(
        user_id=user_id,
        access_token=safe_access_token,
        full_name=full_name,
        email=email,
        expires_at=expires_at
    )

    return {"user_id": user_id, "access_token": safe_access_token}


@app.get("/get_me")
async def get_me(user=Depends(get_user)):
    return user

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
