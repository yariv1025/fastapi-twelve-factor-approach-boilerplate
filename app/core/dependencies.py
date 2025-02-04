from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import decode_access_token
from app.database.models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Security(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return payload  # In a real app, query the DB to get the user object

def require_role(required_role: UserRole):
    """Dependency to restrict access based on user role."""
    async def role_dependency(user: dict = Depends(get_current_user)):
        # if user["role"] != required_role.value:
        if user.get("role") != required_role.value:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return role_dependency