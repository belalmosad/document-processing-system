from fastapi import Depends, APIRouter, HTTPException, status
from core.config import Config
from api.services.authentication import AuthenticationService
from core.dependencies import get_auth_service
from api.schemas.admin import AdminLogin, AdminLoginResponse

router = APIRouter()

@router.post("/login")
def admin_login_route(
    admin_login: AdminLogin, 
    authentication_service: AuthenticationService = Depends(get_auth_service)) -> AdminLoginResponse:
    if(admin_login.admin_cred != Config.SA_CRED):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    access_token = authentication_service.create_access_token({"role": "admin"})
    return {"access_token": access_token}
    