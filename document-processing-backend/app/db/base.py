from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def import_models():
    from .models.audit_trail import AuditTrail
    from .models.document_metadata import DocumentMetadata
    from .models.document_user_permissions import DocumentUserPermission
    from .models.user import User
