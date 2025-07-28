from pydantic import BaseModel, Field
from typing import List
from datetime import date, time

# Input schema for Customer info (nested inside InvoiceIn)
class CustomerIn(BaseModel):
    customer_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    address: str = Field(...)

# Schema for each product item in the invoice
class ProductItem(BaseModel):
    product_code: str
    product_name: str
    category: str
    product_id: int
    quantity: int
    price_per_unit: float
    discount: float
    gst_percent: float

# Invoice creation input schema
class InvoiceIn(BaseModel):
    customer: CustomerIn
    items: List[ProductItem]
    discount_percentage: float = 0.0
    payment_mode: str

# Output schema for Invoice
class InvoiceOut(BaseModel):
    invoice_id: str
    date: date
    time: time  # fixed capital 'T' → lowercase 'time'
    customer: CustomerIn
    items: List[ProductItem]
    total_before_tax: float
    gst_amount: float
    taxable_amount: float
    total_amount: float
    discount: float
    final_total_after_discount: float
    payment_mode: str

    class Config:
        from_attributes = True
