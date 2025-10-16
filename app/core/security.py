import os
from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #현재 시각 + 만료시간 하는거임
    to_encode.update({"exp": expire})  # JWT에 만료시간 추가하는거임
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return expire, token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        is_admin = payload.get("is_admin", False)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"email": email, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(current_user=Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자만 접근할 수 있습니다."
        )
    return current_user