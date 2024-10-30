import os
from db.session import engine
from db.base import Base
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from api.routers import user, document, admin
from db.base import import_models
from middleware.exception_handling import ExceptionHandlingMiddleware
from middleware.custom_response import CustomResponseMiddleware
from middleware.audit_trail import AuditTrailMiddleware
from core.config import Config
from integrations import external_api
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(ExceptionHandlingMiddleware)
app.add_middleware(CustomResponseMiddleware)
app.add_middleware(AuditTrailMiddleware)
# Configure CORS
print(Config.ALLOWED_ORIGIN)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import_models() 

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(external_api.router, prefix="/extra", tags=["External"])

openapi_schema = app.openapi()
openapi_schema["components"]["securitySchemes"] = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
for path in openapi_schema["paths"].values():
    for method in path.values():
        method["security"] = [{"BearerAuth": []}]

app.openapi_schema = openapi_schema

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.RELOAD)