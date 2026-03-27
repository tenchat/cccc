"""
企业模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Company(Base):
    """企业模型"""
    __tablename__ = "companies"

    company_id = Column(String(20), primary_key=True)
    account_id = Column(String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False, unique=True)
    company_name = Column(String(100), nullable=False)
    company_type = Column(String(50))  # 企业类型
    industry = Column(String(50))  # 所属行业
    scale = Column(String(20))  # 规模

    city = Column(String(50))  # 总部城市
    address = Column(String(255))  # 详细地址
    business_license = Column(String(255))  # 营业执照URL

    contact_person = Column(String(50))  # 联系人
    contact_phone = Column(String(20))  # 联系电话
    contact_email = Column(String(100))  # 联系邮箱

    description = Column(Text)  # 企业简介

    verified = Column(Boolean, default=False)  # 是否认证
    verified_at = Column(DateTime, nullable=True)  # 认证时间
    verified_by = Column(String(20), nullable=True)  # 认证人

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    account = relationship("Account", back_populates="company")
    jobs = relationship("JobDescription", back_populates="company")

    def to_dict(self, detailed: bool = False) -> dict:
        """转换为字典"""
        data = {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "industry": self.industry,
            "scale": self.scale,
            "city": self.city,
            "verified": self.verified,
        }

        if detailed:
            data.update({
                "company_type": self.company_type,
                "address": self.address,
                "contact_person": self.contact_person,
                "contact_phone": self.contact_phone,
                "description": self.description,
            })

        return data
