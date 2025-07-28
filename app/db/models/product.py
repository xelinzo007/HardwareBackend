# app/db/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255))
    product_code = Column(String(100))
    category = Column(String(100))
    supplier = Column(String(100))
    quantity = Column(Integer)
    gst = Column(Float)
    mrp = Column(Float)
    selling_price = Column(Float)
    dealer_price = Column(Float)
