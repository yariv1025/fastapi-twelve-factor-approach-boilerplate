import logging

from http import HTTPStatus
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Security

from app.core.config import settings
from app.database.models.scan import Scan
from app.database.models.user import User
from app.database.db_instance import get_db
from app.database.models.user import UserRole
from app.core.auth import decode_access_token
from app.services.auth_service import AuthService
from app.services.scan_service import ScanService
from app.services.user_service import UserService
from app.database.repositories.mongo_repository import MongoRepository
from app.database.repositories.postgres_repository import PostgresRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Dependency to get the payload fo the current user.
    :param token: the access token returned from the security dependency oauth2.
    :return:
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid authentication credentials")
    return payload  # In a real app, query the DB to get the user object


def require_role(required_role: UserRole):
    """Dependency to restrict access based on user role."""

    async def role_dependency(user: dict = Depends(get_current_user)):
        if user.get("role") != required_role.value:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permission denied")
        return user

    return role_dependency



def get_repository(model, db) -> Union[PostgresRepository, MongoRepository]:
    """
    Factory function that dynamically selects and returns the
    appropriate repository class based on the configured database type.

    :param model: SQLAlchemy model (for PostgreSQL) or collection name (for MongoDB).
    :param db: Database session.
    :return: Repository instance.
    """
    if settings.DB_TYPE == "postgres":
        return PostgresRepository(session=db, model=model)
    elif settings.DB_TYPE == "mongodb":
        return MongoRepository(db=db, collection_name=model.__tablename__)
    else:
        logging.error(f"Unsupported database type: {settings.DB_TYPE}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database type not supported")


async def get_service(service_class, model, db) -> Union[UserService, AuthService, ScanService]:
    """
    Factory function to return a service instance dynamically.
    # TODO: is it a FACTORY?

    :param service_class: The service class (UserService, AuthService, etc.).
    :param model: The corresponding model (User, Scan, etc.).
    :param db: Database session.
    :return: Service instance.
    """
    repository = get_repository(model, db)
    return service_class(repository)


# Use the factory function for different services
async def get_user_service(db=Depends(get_db)) -> UserService:
    return await get_service(UserService, User, db)

async def get_auth_service(db=Depends(get_db)) -> AuthService:
    # TODO; check if Auth model should be here instead of User
    return await get_service(AuthService, User, db)

async def get_scan_service(db=Depends(get_db)) -> ScanService:
    return await get_service(ScanService, Scan, db)