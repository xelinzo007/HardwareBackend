from datetime import datetime
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    invoices = relationship("Invoice", back_populates="customer")
    
