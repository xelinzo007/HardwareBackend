from pydantic import BaseModel
from typing import List
from datetime import datetime

class CustomerIn(BaseModel):
    customer_name: str
    phone: str
    address: str

class ProductItem(BaseModel):
    product_code: str
    product_name: str
    category: str
    quantity: int
    price_per_unit: float
    discount: float
    gst_percent: float

class InvoiceIn(BaseModel):
    customer: CustomerIn
    items: List[ProductItem]
    discount_percentage: float = 0.0
    payment_mode: str

class InvoiceOut(BaseModel):
    invoice_id: str
    date: datetime
    customer: CustomerIn
    items: List[ProductItem]
    total_before_tax: float
    gst_amount: float
    taxable_amount: float
    total_amount: float
    discount: float
    final_total_after_discount: float
    payment_mode: str