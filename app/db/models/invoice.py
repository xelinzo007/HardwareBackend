from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String)
    phone = Column(String)
    address = Column(String)
    payment_mode = Column(String)
    total_before_tax = Column(Float)
    gst_amount = Column(Float)
    taxable_amount = Column(Float)
    discount = Column(Float)
    final_total_after_discount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    items = relationship("InvoiceItem", back_populates="invoice")