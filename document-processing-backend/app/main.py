import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from api.routers import user, document
from db.base import import_models
from middleware.exception_handling import ExceptionHandlingMiddleware


app = FastAPI()
app.add_middleware(ExceptionHandlingMiddleware)
import_models() 

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(document.router, prefix="/api/v1/documents", tags=["Documents"])

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 3001)), reload=os.getenv("DEBUG"))