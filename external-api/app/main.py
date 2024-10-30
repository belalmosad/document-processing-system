import os
from fastapi import FastAPI
import uvicorn
from core.config import Config
from api.routes import additional_metadata

app = FastAPI()
app.include_router(additional_metadata.route, prefix="/external")

HOST = Config.HOST
PORT = Config.PORT
DEBUG = Config.DEBUG

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)