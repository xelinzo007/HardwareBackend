# app/db/models/customer.py

from sqlalchemy import Column, Integer, String
from app.db.base import Base  # Make sure this Base is shared across all models

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
