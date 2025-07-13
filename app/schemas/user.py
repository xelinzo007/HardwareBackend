from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., regex="^(Admin|User)$")
    permissions: List[str] = []

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    permissions: List[str]

    class Config:
        orm_mode = True
