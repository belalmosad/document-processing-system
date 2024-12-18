from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from db.base import Base

class DocumentMetadata(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_type = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    mime_type = Column(String, nullable=True)
    keywords = Column(JSONB, nullable=True)
    filename = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    processing_status = Column(String, nullable=True)

    author = relationship("User", back_populates="documents")
    user_permissions = relationship("DocumentUserPermission", back_populates="document")


