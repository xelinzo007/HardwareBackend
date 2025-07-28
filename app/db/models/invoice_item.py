from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_code = Column(String(100))
    product_name = Column(String(255))
    category = Column(String(100))
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    gst_percent = Column(Float)
    discount = Column(Float)

    invoice = relationship("Invoice", back_populates="items")
