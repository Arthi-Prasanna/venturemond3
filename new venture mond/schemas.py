from pydantic import BaseModel
from typing import Optional, List

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str = "client"

class UserCreate(UserBase):
    password: str
    company_name: Optional[str] = None  # For client registration
    project_name: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Dashboard Data Schemas
class DashboardStats(BaseModel):
    total_revenue: float = 0.0
    active_projects: int = 0
    pending_invoices: int = 0
    clients_count: int = 0

class ClientDashboardSchema(BaseModel):
    project_name: str
    status: str
    budget: str
    pending_invoices_count: int
    active_orders_count: int
