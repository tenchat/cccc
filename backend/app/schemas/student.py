"""
学生Schema
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class StudentProfileBase(BaseModel):
    """学生档案基础"""
    student_id: Optional[str] = None
    university_id: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    live_city: Optional[str] = None
    desire_city: Optional[str] = None
    desire_industry: Optional[str] = None
    desire_jd_type: Optional[str] = None
    desire_salary_id: Optional[int] = None
    cur_industry: Optional[str] = None
    cur_jd_type: Optional[str] = None
    cur_salary: Optional[int] = None
    age: Optional[int] = None
    experience: Optional[str] = None
    resume_url: Optional[str] = None


class StudentProfileCreate(StudentProfileBase):
    """创建学生档案"""
    student_id: str  # 必填
    college: str  # 必填
    major: str  # 必填


class StudentProfileUpdate(BaseModel):
    """更新学生档案"""
    student_id: Optional[str] = None
    university_id: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    live_city: Optional[str] = None
    desire_city: Optional[str] = None
    desire_industry: Optional[str] = None
    desire_jd_type: Optional[str] = None
    desire_salary_id: Optional[int] = None
    cur_industry: Optional[str] = None
    cur_jd_type: Optional[str] = None
    cur_salary: Optional[int] = None
    age: Optional[int] = None
    experience: Optional[str] = None
    resume_url: Optional[str] = None


class StudentProfileResponse(StudentProfileBase):
    """学生档案响应"""
    account_id: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """学生列表响应"""
    total: int
    items: List[StudentProfileResponse]
