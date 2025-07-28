from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from app.db.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    def get_ist_date():
        ist = timezone("Asia/Kolkata")
        return datetime.now(ist).date()

    def get_ist_time():
        ist = timezone("Asia/Kolkata")
        return datetime.now(ist).time()

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
    date = Column(Date, default=get_ist_date)
    time = Column(Time, default=get_ist_time)

    items = relationship("InvoiceItem", back_populates="invoice")
