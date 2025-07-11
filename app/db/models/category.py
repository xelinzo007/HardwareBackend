from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String(50), unique=True, nullable=False)
    category_name = Column(String(100), unique=True, nullable=False)
