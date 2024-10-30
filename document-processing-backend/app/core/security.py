from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy import exists, or_
from api.services.authentication import AuthenticationService
from core.dependencies import get_auth_service
from sqlalchemy.orm import Session
from db.models.document_metadata import DocumentMetadata
from db.models.document_user_permissions import DocumentUserPermission
from db.session import get_db


async def get_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    token = auth_header.split(" ")[1]
    return token


async def auth_guard(
    request: Request,
    token: str = Depends(get_token_from_header), 
    auth_service: AuthenticationService = Depends(get_auth_service)):
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    request.state.user = payload
    return payload

async def authorize_to_show_document(request: Request, document_id: int, session: Session = Depends(get_db)):
    if "role" in request.state.user and request.state.user["role"] == "admin":
        return True
    user_id = request.state.user["user_id"]
    is_authorized = session.query(
        exists().where(
            or_(
                DocumentMetadata.author_id == user_id,
                session.query(DocumentUserPermission).filter_by(
                    document_id=document_id, user_id=user_id
                ).exists()
            )
        )
    ).scalar()
    
    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access required to this document"
        )
    return is_authorized

async def authorize_admin(request: Request):
    user = getattr(request.state, 'user', {})
    if "role" not in user or user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action"
        )
    return True