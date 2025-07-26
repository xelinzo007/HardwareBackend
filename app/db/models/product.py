from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    product_code = Column(String, index=True)  # ✅ Removed unique=True
    category = Column(String)
    supplier = Column(String)
    quantity = Column(Integer)
    gst = Column(Float)
    mrp = Column(Float)
    selling_price = Column(Float)
    dealer_price = Column(Float)
