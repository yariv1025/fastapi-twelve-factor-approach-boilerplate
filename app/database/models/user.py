from sqlalchemy import Column, Integer, String, Enum
from app.database.base import BaseRepository
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseRepository):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)  # Default role is "user"
