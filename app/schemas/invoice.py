from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class CustomerIn(BaseModel):
    customer_name: str
    phone: str
    address: str
    model_config = {
        "from_attributes": True
    }

class ProductItem(BaseModel):
    product_id: int
    product_name: str
    category: Optional[str]
    quantity: int
    price_per_unit: float
    discount: float = 0
    gst_percent: float = 0
    model_config = {
        "from_attributes": True
    }

class InvoiceIn(BaseModel):
    customer: CustomerIn
    items: List[ProductItem]
    payment_mode: str
    discount_percentage: float = 0
    model_config = {
        "from_attributes": True
    }

class InvoiceOut(BaseModel):
    invoice_id: str
    date: date
    time: time
    customer: CustomerIn
    items: List[ProductItem]
    total_before_tax: float
    gst_amount: float
    taxable_amount: float
    discount: float
    final_total_after_discount: float
    payment_mode: str
    model_config = {
        "from_attributes": True
    }
