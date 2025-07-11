
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from datetime import datetime
from enum import Enum as PyEnum
from app.db.base import Base

class TransactionType(PyEnum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    type = Column(Enum(TransactionType))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
