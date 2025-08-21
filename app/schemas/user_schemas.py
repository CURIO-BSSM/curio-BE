from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str
    email: str

class UserCreateOut(BaseModel):
    message:str
    user_id:int


class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: str