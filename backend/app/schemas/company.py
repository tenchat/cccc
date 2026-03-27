"""
企业Schema
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class CompanyProfileBase(BaseModel):
    """企业档案基础"""
    company_name: Optional[str] = None
    company_type: Optional[str] = None
    industry: Optional[str] = None
    scale: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    description: Optional[str] = None


class CompanyProfileCreate(CompanyProfileBase):
    """创建企业档案"""
    company_name: str  # 必填


class CompanyProfileUpdate(BaseModel):
    """更新企业档案"""
    company_name: Optional[str] = None
    company_type: Optional[str] = None
    industry: Optional[str] = None
    scale: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    description: Optional[str] = None


class CompanyProfileResponse(CompanyProfileBase):
    """企业档案响应"""
    company_id: str
    account_id: str
    verified: bool = False

    class Config:
        from_attributes = True


class CompanyVerifyRequest(BaseModel):
    """企业审核请求"""
    company_id: str
    action: str = Field(..., pattern=r"^(approve|reject)$")
    reason: Optional[str] = None


class CompanyListResponse(BaseModel):
    """企业列表响应"""
    total: int
    items: List[CompanyProfileResponse]
