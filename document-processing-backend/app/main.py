import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from api.routers import user, document, admin
from db.base import import_models
from middleware.exception_handling import ExceptionHandlingMiddleware
from middleware.custom_response import CustomResponseMiddleware
from middleware.audit_trail import AuditTrailMiddleware
from core.config import Config



app = FastAPI()
app.add_middleware(ExceptionHandlingMiddleware)
app.add_middleware(CustomResponseMiddleware)
app.add_middleware(AuditTrailMiddleware)

import_models() 

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(document.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.RELOAD)