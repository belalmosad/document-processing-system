from fastapi import APIRouter

router = APIRouter()
@router.get("/")
def getUser():
    return {"Hello": "doc"}