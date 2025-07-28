from typing import Text
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time,text
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from app.db.base import Base

def get_ist_date():
    ist = timezone("Asia/Kolkata")
    return datetime.now(ist).date()

def get_ist_time():
    ist = timezone("Asia/Kolkata")
    return datetime.now(ist).time()

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(100))
    phone = Column(String(20))
    address = Column(text)
    date = Column(Date, default=datetime.utcnow)
    time = Column(Time, default=datetime.utcnow().time)
    payment_mode = Column(String(50))
    total_before_tax = Column(Float)
    gst_amount = Column(Float)
    taxable_amount = Column(Float)
    discount = Column(Float)
    final_total_after_discount = Column(Float)

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
