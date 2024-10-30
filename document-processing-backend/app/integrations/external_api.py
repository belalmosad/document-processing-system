import requests
from core.config import Config
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/{document_id}")
def get_additional_info_route(document_id: int):
    return get_additional_document_info(document_id)
    
def get_additional_document_info(document_id):
    url = Config.EXTERNAL_API_URL + "/external/additional/" + f"{document_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Something wen wrong integrating with external service"
    )
    
    