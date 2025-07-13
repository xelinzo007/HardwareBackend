from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'Admin' or 'User'
    created_at = Column(DateTime, default=datetime.utcnow)

    permissions = relationship("UserPermission", back_populates="user", cascade="all, delete-orphan")


class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_name = Column(String, nullable=False)  # e.g., "view_dashboard"

    user = relationship("User", back_populates="permissions")
