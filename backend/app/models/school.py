"""
学校模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class University(Base):
    """院校模型"""
    __tablename__ = "universities"

    university_id = Column(String(20), primary_key=True)  # 院校代码
    university_name = Column(String(100), nullable=False)
    province = Column(String(20))  # 所在省份
    city = Column(String(50))  # 所在城市
    university_type = Column(String(50))  # 院校类型
    admin_level = Column(String(20))  # 主管单位

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    school_admins = relationship("SchoolAdmin", back_populates="university")
    student_profiles = relationship("StudentProfile", back_populates="university")


class SchoolAdmin(Base):
    """学校管理员关联"""
    __tablename__ = "school_admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    university_id = Column(String(20), ForeignKey('universities.university_id', ondelete='CASCADE'), nullable=False)
    is_primary = Column(Integer, default=0)  # 是否主管理员

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    account = relationship("Account", back_populates="school_admin")
    university = relationship("University", back_populates="school_admins")
