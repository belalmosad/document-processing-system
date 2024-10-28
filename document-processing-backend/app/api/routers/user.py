from fastapi import APIRouter, Depends
from api.services.user import UserService
from api.schemas.user import UserCreate
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter()

@router.post("/")
def create_user_router(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.create_user(user)
    return {
        "Success": True,
        "Message": f"User {db_user.username} successfully created"
    }