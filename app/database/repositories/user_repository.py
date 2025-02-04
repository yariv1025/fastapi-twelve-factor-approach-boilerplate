from sqlalchemy.orm import Session
from app.database.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user_data: dict):
        """Create a new user and store it in the database."""
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    async def get_by_email(self, email: str):
        """Retrieve a user by email."""
        return self.session.query(User).filter(User.email == email).first()

    async def get_by_id(self, user_id: int):
        """Retrieve a user by ID."""
        return self.session.query(User).filter(User.id == user_id).first()
