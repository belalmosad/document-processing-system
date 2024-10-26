import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn


app = FastAPI()
load_dotenv()

@app.get("/")
def read_root():
    return {"Hello": "From another backend"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 3001)), reload=os.getenv("DEBUG"))