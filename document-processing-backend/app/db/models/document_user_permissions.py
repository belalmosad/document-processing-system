from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class DocumentUserPermission(Base):
    __tablename__ = "document_user_permissions"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), primary_key=True, nullable=False)
    permission = Column(String, nullable=False)

    user = relationship("User", back_populates="document_permissions")
    document = relationship("DocumentMetadata", back_populates="user_permissions")
