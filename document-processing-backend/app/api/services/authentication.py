from datetime import datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv
from core.config import Config

class AuthenticationService:
    load_dotenv()
    ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
    SECRET_KEY = Config.SECRET_KEY
    ALGORITHM=Config.ALGORITHM

    def create_access_token(self, data: dict):
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        access_token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return access_token

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.PyJWTError: 
            return None