"""
账户Schema
"""
from typing import Optional
from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    """账户基础"""
    username: str
    real_name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class AccountUpdate(BaseModel):
    """账户更新"""
    real_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = None


class AccountResponse(BaseModel):
    """账户响应"""
    account_id: str
    username: str
    real_name: str
    role: str
    status: str

    class Config:
        from_attributes = True
