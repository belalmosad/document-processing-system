from fastapi import APIRouter, Depends
from core.dependencies import get_document_service
from api.services.document import DocumentService

router = APIRouter()

@router.post("/upload")
def upload_and_process_document_router(document_data, document_service: DocumentService = Depends(get_document_service)):
    return document_service.process_document("pdf", document_data)