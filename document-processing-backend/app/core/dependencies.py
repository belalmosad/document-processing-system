from fastapi import Depends
from api.services.user import UserService
from api.services.authentication import AuthenticationService
from sqlalchemy.orm import Session
from db.session import get_db

def get_auth_service():
    return AuthenticationService()

def get_user_service(
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)):
    return UserService(db, auth_service)
