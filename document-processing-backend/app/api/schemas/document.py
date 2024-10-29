from collections import defaultdict
from pydantic import BaseModel



class DocumentMetadataResponse(BaseModel):
    id: int
    document_type: str
    author_id: int
    keywords: defaultdict[str, int]
    filename: str
    size: float
    processing_status: str

    class Config:
        orm_mode = True