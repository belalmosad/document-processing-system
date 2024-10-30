from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", "3001"))
    HOST = os.getenv("HOST")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")