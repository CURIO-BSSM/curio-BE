from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    message: str
    user_id: int
    access_token: str
    token_type: str
    expires_in: str

class UserLogout(BaseModel):
    access_token: str
