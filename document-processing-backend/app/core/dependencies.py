from fastapi import Depends
from api.services.user import UserService
from api.services.authentication import AuthenticationService
from api.services.document import DocumentFactory, DocumentService
from sqlalchemy.orm import Session
from db.session import get_db
from api.services.audit_trail import AuditTrailService

def get_auth_service():
    return AuthenticationService()

def get_user_service(
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)):
    return UserService(db, auth_service)

def get_document_factory():
    return DocumentFactory()

def get_document_service(
    db: Session = Depends(get_db),
    document_factory: DocumentFactory = Depends(get_document_factory)):
    return DocumentService(db, document_factory)

def get_audit_trail_service(db: Session = Depends(get_db)):
    return AuditTrailService(db)