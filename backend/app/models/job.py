"""
岗位模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class JobDescription(Base):
    """岗位需求模型"""
    __tablename__ = "job_descriptions"

    jd_no = Column(String(20), primary_key=True)  # 职位代码
    company_id = Column(String(20), ForeignKey('companies.company_id', ondelete='CASCADE'), nullable=False)
    jd_title = Column(String(100), nullable=False)  # 职位标题
    city = Column(String(50), nullable=False)  # 工作城市
    jd_sub_type = Column(String(50))  # 职位子类
    industry = Column(String(50))  # 所属行业

    require_nums = Column(Integer, default=1)  # 需求人数
    max_salary = Column(Integer)  # 最高月薪
    min_salary = Column(Integer)  # 最低月薪

    start_date = Column(Date)  # 开始日期
    end_date = Column(Date)  # 结束日期
    is_travel = Column(Boolean, default=False)  # 是否出差

    min_years = Column(String(10))  # 工作年限
    key_words = Column(String(255))  # 关键字

    min_edu_level = Column(Integer)  # 最低学历
    max_edu_level = Column(Integer)  # 最高学历

    is_mangerial = Column(Boolean, default=False)  # 是否要求管理经验
    resume_language_required = Column(String(50))  # 语言需求

    job_description = Column(Text)  # 职位描述

    status = Column(String(20), default="active")  # 状态 active/closed
    view_count = Column(Integer, default=0)  # 浏览次数
    apply_count = Column(Integer, default=0)  # 申请次数

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    company = relationship("Company", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "jd_no": self.jd_no,
            "jd_title": self.jd_title,
            "company_name": self.company.company_name if self.company else None,
            "city": self.city,
            "industry": self.industry,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "min_edu_level": self.min_edu_level,
            "job_description": self.job_description,
            "status": self.status,
        }


class JobApplication(Base):
    """岗位申请记录"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jd_no = Column(String(20), ForeignKey('job_descriptions.jd_no', ondelete='CASCADE'), nullable=False)
    account_id = Column(String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)

    resume_url = Column(String(255))  # 投递的简历
    cover_letter = Column(Text)  # 求职信

    status = Column(String(20), default="pending")  # pending/viewed/interview/rejected/offered

    remark = Column(Text)  # 备注
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    job = relationship("JobDescription", back_populates="applications")
    account = relationship("Account")

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "jd_no": self.jd_no,
            "account_id": self.account_id,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }
