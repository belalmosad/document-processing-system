
from pydantic import BaseModel


class AdminLogin(BaseModel):
    admin_cred: str

class AdminLoginResponse(BaseModel):
    access_token: str
