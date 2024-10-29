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

@router.get("/metadata/{document_id}")
def get_document_metadata_by_id_router(document_id: int, document_service: DocumentService = Depends(get_document_service)):
    return document_service.get_document_metadata_by_document_id(document_id)

@router.get("/metadata/author/all")
def get_document_metadata_by_author_id_router(document_service: DocumentService = Depends(get_document_service)):
    return document_service.get_document_by_author_id(28)