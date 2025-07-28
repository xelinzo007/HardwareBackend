from pydantic import BaseModel
from typing import Optional

class InvoiceItemOut(BaseModel):
    product_code: str
    product_name: str
    category: Optional[str]
    quantity: int
    price_per_unit: float
    discount: float
    gst_percent: float

    model_config = {
        "from_attributes": True
    }

class ProductItem(BaseModel):  # Used for InvoiceIn
    product_id: int
    quantity: int
    price_per_unit: Optional[float] = None
    discount: Optional[float] = 0.0

    model_config = {
        "from_attributes": True
    }