from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class DocumentUserPermission(Base):
    __tablename__ = "document_user_permissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    permission = Column(String, nullable=False)

    user = relationship("User", back_populates="document_permissions")
    document = relationship("DocumentMetadata", back_populates="user_permissions")
