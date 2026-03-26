from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EmploymentStatus(str, Enum):
    UNEMPLOYED = "0"  # 待业
    EMPLOYED = "1"  # 就业
    FURTHER_STUDY = "2"  # 升学
    ABROAD = "3"  # 出国


class StudentBase(BaseModel):
    student_id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=50)
    college: str = Field(..., max_length=50)
    major: str = Field(..., max_length=50)
    grade: str = Field(..., max_length=10)
    province: str = Field(..., max_length=20)
    gpa: Optional[float] = None
    employment_status: str = "0"
    salary: Optional[int] = None
    company: Optional[str] = None
    position: Optional[str] = None
    skills: Optional[str] = None
    internship: Optional[str] = None
    target_city: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    grade: Optional[str] = None
    province: Optional[str] = None
    gpa: Optional[float] = None
    employment_status: Optional[str] = None
    salary: Optional[int] = None
    company: Optional[str] = None
    position: Optional[str] = None
    skills: Optional[str] = None
    internship: Optional[str] = None
    target_city: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[StudentResponse]