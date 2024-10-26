from typing import List, Optional

from pydantic import BaseModel


class DocumentMetadataResponse(BaseModel):
    id: int
    document_type: str
    author_id: int
    keywords: Optional[dict] = None
    filename: str
    size: float
    processing_status: str

    class Config:
        orm_mode = True