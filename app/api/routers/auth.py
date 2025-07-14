# from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordBearer
# from fastapi.security import OAuth2PasswordRequestForm
# from app.schemas.token import Token
# from app.core.security import verify_token
# from fastapi import Request
# from app.core.security import create_access_token
# from datetime import timedelta

# router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# fake_user = {
#     "username": "admin",
#     "password": "admin123"  # Use hashed in real case
# }

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(data={"sub": fake_user["username"]}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/protected")
# def protected_route(token: str = Depends(oauth2_scheme)):
#     username = verify_token(token)
#     if not username:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return {"message": f"Hello, {username}. You are authorized."}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

