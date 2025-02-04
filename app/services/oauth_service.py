from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import RedirectResponse
from app.core.config import settings
from app.services.auth_service import AuthService
from app.database.repositories.user_repository import UserRepository
from app.database.session import get_pg_session

oauth = OAuth()

# Configure OAuth providers
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "user:email"},
)

router = APIRouter()

@router.get("/login/{provider}")
async def oauth_login(provider: str, request: Request):
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    redirect_uri = settings.OAUTH_REDIRECT_URI
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def oauth_callback(provider: str, request: Request, session=Depends(get_pg_session)):
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    user_info = await client.parse_id_token(request, token) if provider == "google" else token["access_token"]

    auth_service = AuthService(UserRepository(session))
    user = await auth_service.oauth_login(user_info, provider)

    return {"access_token": user["access_token"], "token_type": "bearer"}
