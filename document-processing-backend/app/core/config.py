import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "3001"))
    RELOAD: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    DB_URL: str = os.getenv("DB_URL")
