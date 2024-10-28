from api.schemas.user import UserCreate
from sqlalchemy.orm import Session
from db.models.user import User

def create_user(db: Session, user_data: UserCreate) -> User:
    try:
        db_user = User(
        username = user_data.username,
        role = user_data.role,
        passwordHash = user_data.password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise Exception("Something went wrong")
    