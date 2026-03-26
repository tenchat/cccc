from sqlalchemy import Column, Integer, String, DECIMAL, SmallInteger, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(20), unique=True, index=True, nullable=False, comment="学号")
    name = Column(String(50), nullable=False, comment="姓名")
    college = Column(String(50), nullable=False, comment="学院")
    major = Column(String(50), nullable=False, comment="专业")
    grade = Column(String(10), nullable=False, comment="届次")
    province = Column(String(20), nullable=False, comment="生源省份")
    gpa = Column(DECIMAL(3, 2), nullable=True, comment="GPA")
    employment_status = Column(SmallInteger, default=0, comment="就业状态: 0待业 1就业 2升学 3出国")
    salary = Column(Integer, nullable=True, comment="起薪")
    company = Column(String(100), nullable=True, comment="就业公司")
    position = Column(String(50), nullable=True, comment="岗位")
    skills = Column(Text, nullable=True, comment="技能证书(JSON)")
    internship = Column(Text, nullable=True, comment="实习经历")
    target_city = Column(String(50), nullable=True, comment="目标城市")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())