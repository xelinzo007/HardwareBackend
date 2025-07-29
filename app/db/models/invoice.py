from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(20), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String(100))
    phone = Column(String(15))
    address = Column(String(255))
    payment_mode = Column(String(50))

    total_before_tax = Column(Float)
    gst_amount = Column(Float)
    taxable_amount = Column(Float)
    discount = Column(Float)
    final_total_after_discount = Column(Float)

    created_at = Column(DateTime, default=datetime.now)

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
