from fastapi import Depends, HTTPException, Request, status
from api.services.authentication import AuthenticationService
from core.dependencies import get_auth_service

async def get_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    token = auth_header.split(" ")[1]
    return token


async def auth_guard(token: str = Depends(get_token_from_header), auth_service: AuthenticationService = Depends(get_auth_service)):
    payload = auth_service.verify_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return payload
