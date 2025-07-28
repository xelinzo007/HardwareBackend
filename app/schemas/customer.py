from pydantic import BaseModel, Field
from typing import Optional

class CustomerCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    address: Optional[str] = None

class CustomerOut(CustomerCreate):
    id: int

    class Config:
        from_attributes = True
