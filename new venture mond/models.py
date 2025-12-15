from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # 'admin' or 'client'
    is_active = Column(Boolean, default=True)

    # Relationships
    client_profile = relationship("ClientProfile", back_populates="user", uselist=False)

class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String)
    project_name = Column(String)
    budget = Column(String)
    status = Column(String, default="Pending") # Active, Pending, Delayed
    
    user = relationship("User", back_populates="client_profile")
    invoices = relationship("Invoice", back_populates="client")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("client_profiles.id"))
    amount = Column(Float)
    date_issued = Column(DateTime, default=datetime.utcnow)
    status = Column(String) # Paid, Pending, Overdue

    client = relationship("ClientProfile", back_populates="invoices")
