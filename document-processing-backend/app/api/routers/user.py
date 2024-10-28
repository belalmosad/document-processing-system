from fastapi import APIRouter, Depends
from api.services.user import create_user
from api.schemas.user import UserCreate
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter()

@router.post("/")
def create_user_router(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return {
        "Success": True
    }