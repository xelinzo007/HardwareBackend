from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time
from app.schemas.customer import CustomerIn
from app.schemas.product_item import ProductItem
from app.schemas.invoice_item import InvoiceItemOut

class InvoiceIn(BaseModel):
    customer: CustomerIn
    items: List[ProductItem]
    payment_mode: str
    discount_percentage: Optional[float] = 0.0
    model_config = {
        "from_attributes": True
    }

class InvoiceOut(BaseModel):
    invoice_id: str
    date: date
    time: time
    customer: CustomerIn
    items: List[InvoiceItemOut]
    total_before_tax: float
    gst_amount: float
    taxable_amount: float
    total_amount: float
    discount: float
    final_total_after_discount: float
    payment_mode: str

    model_config = {
        "from_attributes": True
    }
