from fastapi import HTTPException, status
from api.schemas.user import UserCreate, UserLogin, UserResponse
from sqlalchemy.orm import Session
from db.models.user import User
from api.services.authentication import AuthenticationService
import bcrypt

class UserService:
    def __init__(self, db: Session, authentication_service: AuthenticationService):
        self.db = db
        self.authentication_service = authentication_service
        
    def create_user(self, user_data: UserCreate):
        if(self.username_exists(user_data.username)):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists")
        self.get_user_by_username(user_data.username)
        db_user = User(
        username = user_data.username,
        role = user_data.role,
        passwordHash = self.hash_password(user_data.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def login_user(self, user: UserLogin) -> str: # returns access token
        if(not self.username_exists(user.username)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        db_user = self.get_user_by_username(user.username)
        if(not self.valid_password(user.password, db_user.passwordHash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        access_token = self.authentication_service.create_access_token({
            "user_id": db_user.id,
            "username": db_user.username})
        return access_token

    # Helper functions
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
    
    def hash_password(self, password: str):
        password_bytes = password.encode()
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()
        return hashed_password
    
    def valid_password(self, claimed_password: str, db_password: str) -> bool:
        password_bytes = claimed_password.encode()
        db_password_bytes = db_password.encode()
        return bcrypt.checkpw(password_bytes, db_password_bytes)


