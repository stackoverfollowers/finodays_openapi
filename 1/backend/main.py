import httpx
import uvicorn
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends

from httpx_oauth.clients.google import GoogleOAuth2

from auth.user import get_user, ensure_user_in_db

client = GoogleOAuth2(
    "593847446158-74h9u15qhsenn9vgjfb0474rs8qbhsb0.apps.googleusercontent.com",
    "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")

app = FastAPI()

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = OAuth2(
#     "CLIENT_ID",
#     "CLIENT_SECRET",
#     "AUTHORIZE_ENDPOINT",
#     "ACCESS_TOKEN_ENDPOINT",
#     refresh_token_endpoint="REFRESH_TOKEN_ENDPOINT",
#     revoke_token_endpoint="REVOKE_TOKEN_ENDPOINT",
# )

oauth2_authorize_callback = OAuth2AuthorizeCallback(client, "oauth-callback")


@app.get("/oauth-callback", name="oauth-callback")
async def oauth_callback(access_token_state=Depends(oauth2_authorize_callback)):
    token, _ = access_token_state

    access_token = token["access_token"]

    async with httpx.AsyncClient() as httpx_client:
        url = "https://www.googleapis.com/oauth2/v1/userinfo"
        resp = await httpx_client.get(url, params={
            "alt": "json",
            "access_token": access_token
        })
    resp_json = resp.json()

    expires_at = token["expires_at"]
    safe_access_token = access_token + "_safe!"
    ensure_user_in_db(
        access_token=safe_access_token,
        name=resp_json["name"],
        expires_at=expires_at
    )

    return {"access_token": safe_access_token}


@app.get("/get_auth_url")
async def home():
    authorization_url = await client.get_authorization_url(
        "http://localhost:8000/oauth-callback", scope=[],
    )
    return {'result': authorization_url}


@app.get("/get_me")
async def get_me(user=Depends(get_user)):
    return {
        "name": user["name"],
        "expires_at": user["expires_at"]
    }

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
