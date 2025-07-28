from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)

    # 🔧 Add this to fix the error
    invoices = relationship("Invoice", back_populates="customer")
