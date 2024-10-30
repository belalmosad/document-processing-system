from fastapi import Depends, APIRouter, HTTPException, status
from core.config import Config
from api.services.authentication import AuthenticationService
from core.dependencies import get_auth_service, get_audit_trail_service
from api.schemas.admin import AdminLogin, AdminLoginResponse
from api.services.audit_trail import AuditTrailService
from core.security import authorize_admin, auth_guard

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

@router.get("/audit", dependencies=[Depends(auth_guard), Depends(authorize_admin)])
def get_audit_tril_route(audit_trail_service: AuditTrailService = Depends(get_audit_trail_service)):
    return audit_trail_service.get_audit_trail()