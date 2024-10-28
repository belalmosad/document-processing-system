from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    access_token: str

    class Config:
        orm_mode = True

