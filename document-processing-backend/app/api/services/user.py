from fastapi import HTTPException, status
from api.schemas.user import UserCreate
from sqlalchemy.orm import Session
from db.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        if(self.username_exists(user_data.username)):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists")
        self.get_user_by_username(user_data.username)
        db_user = User(
        username = user_data.username,
        role = user_data.role,
        passwordHash = user_data.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
        
    def get_user_by_username(self, username: str) -> User:
        result: User = self.db.query(User).filter(User.username == username).first()
        if(not result):
            return None
        return result
    
    def username_exists(self, username: str):
        user = self.get_user_by_username(username)
        if(not user):
            return False
        return True

