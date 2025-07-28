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
