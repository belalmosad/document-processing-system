from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    passwordHash = Column(String, nullable=False)
    certSubjectDN = Column(String, nullable=False)

    documents = relationship("DocumentMetadata", back_populates="author")
    document_permissions = relationship("DocumentUserPermission", back_populates="user")
    audit_trails = relationship("AuditTrail", back_populates="user")


