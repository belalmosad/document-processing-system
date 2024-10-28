from api.schemas.user import UserCreate
from sqlalchemy.orm import Session
from db.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        try:
            db_user = User(
            username = user_data.username,
            role = user_data.role,
            passwordHash = user_data.password
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            raise Exception("Something went wrong")
