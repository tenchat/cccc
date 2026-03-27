"""
岗位Schema
"""
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    """岗位基础"""
    jd_title: str
    city: str
    jd_sub_type: Optional[str] = None
    industry: Optional[str] = None
    require_nums: int = 1
    max_salary: Optional[int] = None
    min_salary: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_travel: bool = False
    min_years: Optional[str] = None
    key_words: Optional[str] = None
    min_edu_level: Optional[int] = None
    max_edu_level: Optional[int] = None
    is_mangerial: bool = False
    resume_language_required: Optional[str] = None
    job_description: Optional[str] = None


class JobCreate(JobBase):
    """创建岗位"""
    pass


class JobUpdate(BaseModel):
    """更新岗位"""
    jd_title: Optional[str] = None
    city: Optional[str] = None
    jd_sub_type: Optional[str] = None
    industry: Optional[str] = None
    require_nums: Optional[int] = None
    max_salary: Optional[int] = None
    min_salary: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_travel: Optional[bool] = None
    min_years: Optional[str] = None
    key_words: Optional[str] = None
    min_edu_level: Optional[int] = None
    max_edu_level: Optional[int] = None
    is_mangerial: Optional[bool] = None
    resume_language_required: Optional[str] = None
    job_description: Optional[str] = None
    status: Optional[str] = None


class JobResponse(JobBase):
    """岗位响应"""
    jd_no: str
    company_name: Optional[str] = None
    status: str = "active"
    view_count: int = 0
    apply_count: int = 0

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """岗位列表响应"""
    total: int
    items: List[JobResponse]


class JobApplyRequest(BaseModel):
    """申请岗位请求"""
    jd_no: str
    cover_letter: Optional[str] = None


class JobApplyResponse(BaseModel):
    """申请响应"""
    id: int
    jd_no: str
    status: str
    applied_at: str
    message: str = "申请成功"


class ApplicationResponse(BaseModel):
    """申请记录响应"""
    id: int
    jd_no: str
    company_name: Optional[str] = None
    jd_title: Optional[str] = None
    status: str
    applied_at: str

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """申请列表响应"""
    total: int
    items: List[ApplicationResponse]
