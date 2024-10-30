from fastapi import APIRouter, Depends
from api.services.additional_metadata import AdditionalMetadataService
from core.dependencies import get_additional_metadata_service

route = APIRouter()

@route.get("/additional/{document_id}")
def get_additional_metadata(
    document_id: int, 
    additional_metadata_service: AdditionalMetadataService = Depends(get_additional_metadata_service)):
    return additional_metadata_service.get_additional_metadata(document_id)