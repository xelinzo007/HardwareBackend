from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.db.base import Base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)