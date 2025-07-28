# app/models/invoice.py

from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(100), unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_mode = Column(String(50))
    total_before_tax = Column(Float)
    total_gst = Column(Float)
    total_after_tax = Column(Float)
    discount = Column(Float)
    grand_total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Backref to InvoiceItem
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")
