"""
学生档案模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class StudentProfile(Base):
    """学生档案模型"""
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False, unique=True)
    student_id = Column(String(20), unique=True, nullable=True)  # 学号
    university_id = Column(String(20), nullable=True)  # 院校代码
    college = Column(String(100))  # 学院
    major = Column(String(100))  # 专业
    degree = Column(String(20))  # 学历
    graduation_year = Column(Integer)  # 毕业年份

    # 期望信息
    live_city = Column(String(50))  # 现居住地
    desire_city = Column(String(50))  # 期望工作城市
    desire_industry = Column(String(50))  # 期望行业
    desire_jd_type = Column(String(50))  # 期望职类
    desire_salary_id = Column(Integer)  # 期望薪资ID

    # 当前信息
    cur_industry = Column(String(50))  # 最近工作行业
    cur_jd_type = Column(String(50))  # 最近工作职类
    cur_salary = Column(Integer)  # 最近薪水

    age = Column(Integer)  # 年龄
    start_work_date = Column(Date)  # 开始工作时间
    experience = Column(Text)  # 经验描述

    # 附件
    resume_url = Column(String(255))  # 简历URL

    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    account = relationship("Account", back_populates="student_profile")

    def to_dict(self, masked: bool = False) -> dict:
        """
        转换为字典

        Args:
            masked: 是否脱敏（企业查看时）
        """
        data = {
            "account_id": self.account_id,
            "student_id": self.student_id,
            "university_id": self.university_id,
            "college": self.college,
            "major": self.major,
            "degree": self.degree,
            "graduation_year": self.graduation_year,
            "live_city": self.live_city,
            "desire_city": self.desire_city,
            "desire_industry": self.desire_industry,
            "desire_jd_type": self.desire_jd_type,
            "cur_industry": self.cur_industry,
            "cur_salary": self.cur_salary,
            "resume_url": self.resume_url,
        }

        if masked:
            # 脱敏处理
            data["name"] = self.account.real_name[:1] + "**" if self.account else "未知"
            data["phone"] = None
        else:
            data["name"] = self.account.real_name if self.account else None

        return data
