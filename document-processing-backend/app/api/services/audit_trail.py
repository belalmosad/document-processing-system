from sqlalchemy.orm import Session
from db.models.audit_trail import AuditTrail

class AuditTrailService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_audit_trail(self):
        result = self.db.query(AuditTrail).all()
        return result