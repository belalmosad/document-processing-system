from fastapi import APIRouter, Depends
from api.services.user import UserService
from api.schemas.user import UserCreate, UserLogin, UserResponse
from sqlalchemy.orm import Session
from db.session import get_db
from core.dependencies import get_user_service

router = APIRouter()

@router.post("/signup")
def user_signup_route(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service)):
    db_user = user_service.create_user(user)
    return {
        "Success": True,
        "Message": f"User {db_user.username} successfully created"
    }

@router.post("/login")
def user_login_route(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    access_token = user_service.login_user(user)
    return {"access_token": access_token}
    