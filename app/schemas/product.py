from pydantic import BaseModel, Field

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
