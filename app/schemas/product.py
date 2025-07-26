from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    product_code: str
    category: str
    supplier: str
    quantity: int
    gst: float
    mrp: float
    selling_price: float
    dealer_price: float

    model_config = {
        "from_attributes": True
    }

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    category: Optional[str] = None
    supplier: Optional[str] = None
    quantity: Optional[int] = None
    gst: Optional[float] = None
    mrp: Optional[float] = None
    selling_price: Optional[float] = None
    dealer_price: Optional[float] = None

    model_config = {
        "from_attributes": True
    }
