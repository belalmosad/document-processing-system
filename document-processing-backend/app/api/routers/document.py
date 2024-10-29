from fastapi import APIRouter, Depends, File, UploadFile
from core.dependencies import get_document_service
from api.services.document import DocumentService
from api.schemas.document import DocumentMetadataResponse

router = APIRouter()

@router.post("/upload")
async def upload_and_process_document_router(
    file: UploadFile = File(...), 
    document_service: DocumentService = Depends(get_document_service)) -> DocumentMetadataResponse:
    document_metadata = await document_service.process_document(file)
    return document_metadata