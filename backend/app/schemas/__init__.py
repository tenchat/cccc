"""
Schemas模块 - 请求响应模型层
"""
from .auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserInfo,
    LoginResponse,
    RegisterResponse,
    SessionInfo,
    SessionListResponse,
    ErrorResponse,
)
from .account import (
    AccountBase,
    AccountUpdate,
    AccountResponse,
)
from .student import (
    StudentProfileBase,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
    StudentListResponse,
)
from .company import (
    CompanyProfileBase,
    CompanyProfileCreate,
    CompanyProfileUpdate,
    CompanyProfileResponse,
    CompanyVerifyRequest,
    CompanyListResponse,
)
from .job import (
    JobBase,
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse,
    JobApplyRequest,
    JobApplyResponse,
    ApplicationResponse,
    ApplicationListResponse,
)

__all__ = [
    # auth
    "RegisterRequest",
    "LoginRequest",
    "RefreshTokenRequest",
    "TokenResponse",
    "UserInfo",
    "LoginResponse",
    "RegisterResponse",
    "SessionInfo",
    "SessionListResponse",
    "ErrorResponse",
    # account
    "AccountBase",
    "AccountUpdate",
    "AccountResponse",
    # student
    "StudentProfileBase",
    "StudentProfileCreate",
    "StudentProfileUpdate",
    "StudentProfileResponse",
    "StudentListResponse",
    # company
    "CompanyProfileBase",
    "CompanyProfileCreate",
    "CompanyProfileUpdate",
    "CompanyProfileResponse",
    "CompanyVerifyRequest",
    "CompanyListResponse",
    # job
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobListResponse",
    "JobApplyRequest",
    "JobApplyResponse",
    "ApplicationResponse",
    "ApplicationListResponse",
]
