from datetime import datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv

class AuthenticationService:
    load_dotenv()
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM=os.getenv("JWT_ALGORITHM")

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