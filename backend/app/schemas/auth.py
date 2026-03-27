"""
认证Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8, max_length=32)
    confirm_password: str
    role: str = Field(..., pattern=r"^(student|school_admin|company_admin)$")
    real_name: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("密码必须包含大写字母")
        if not re.search(r"[a-z]", v):
            raise ValueError("密码必须包含小写字母")
        if not re.search(r"[0-9]", v):
            raise ValueError("密码必须包含数字")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("密码必须包含特殊字符(!@#$%^&*等)")
        return v

    @field_validator('confirm_password')
    @classmethod
    def validate_match(cls, v, info):
        if v != info.data.get('password'):
            raise ValueError("两次密码不一致")
        return v


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserInfo(BaseModel):
    """用户信息"""
    account_id: str
    username: str
    real_name: str
    role: str
    status: str
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserInfo


class RegisterResponse(BaseModel):
    """注册响应"""
    account_id: str
    username: str
    real_name: str
    role: str
    status: str
    message: str = "注册成功"


class SessionInfo(BaseModel):
    """会话信息"""
    id: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: str
    last_used_at: Optional[str] = None
    is_current: bool = False


class SessionListResponse(BaseModel):
    """会话列表响应"""
    sessions: List[SessionInfo]
    total: int


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error: dict
