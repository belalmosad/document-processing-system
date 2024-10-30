from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from core.dependencies import get_document_service
from api.services.document import DocumentService
from api.schemas.document import DocumentMetadataResponse, DocumentSearch
from core.security import auth_guard, authorize_to_show_document

router = APIRouter(dependencies=[Depends(auth_guard)])

@router.post("/upload")
async def upload_and_process_document_router(
    file: UploadFile = File(...), 
    document_service: DocumentService = Depends(get_document_service)) -> DocumentMetadataResponse:
    document_metadata = await document_service.process_document(file)
    return document_metadata

@router.get("/metadata/{document_id}", dependencies=[Depends(authorize_to_show_document)])
def get_document_metadata_by_id_router(
    document_id: int, 
    document_service: DocumentService = Depends(get_document_service)):
    return document_service.get_document_metadata_by_document_id(document_id)

@router.get("/metadata/author/all")
def get_document_metadata_by_author_id_router(document_service: DocumentService = Depends(get_document_service)):
    return document_service.get_document_by_author_id(28)

@router.get("/{document_id}", dependencies=[Depends(authorize_to_show_document)])
def get_document_url_router(document_id: int, document_service: DocumentService = Depends(get_document_service)) -> StreamingResponse:
    return document_service.stream_document(document_id)

@router.post("/search")
def search_by_keywords_route(document_search: DocumentSearch,document_service: DocumentService = Depends(get_document_service)):
    keywords = document_search.search.strip().lower().split()
    return document_service.search_by_keywords(keywords)