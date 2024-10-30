from collections import defaultdict
from pydantic import BaseModel


class DocumentSearch(BaseModel):
    search: str

class DocumentMetadataResponse(BaseModel):
    id: int
    document_type: str
    author_id: int
    filename: str
    size: float
    mime_type: str
    processing_status: str

    class Config:
        orm_mode = True