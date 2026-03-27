"""
统一错误处理模块
职责：定义API错误，统一错误响应格式
"""
from fastapi import HTTPException, status
from typing import Optional, Any


class APIError(Exception):
    """API错误基类"""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }

    def to_http_exception(self) -> HTTPException:
        """转换为HTTP异常"""
        return HTTPException(
            status_code=self.status_code,
            detail=self.to_dict()
        )


class Errors:
    """预定义错误"""

    # 认证错误 (1xxx)
    INVALID_CREDENTIALS = APIError(
        code="AUTH_001",
        message="用户名或密码错误",
        status_code=401
    )

    ACCOUNT_LOCKED = APIError(
        code="AUTH_002",
        message="账号已锁定，请{minutes}分钟后重试",
        status_code=423
    )

    TOKEN_EXPIRED = APIError(
        code="AUTH_003",
        message="登录已过期，请重新登录",
        status_code=401
    )

    TOKEN_INVALID = APIError(
        code="AUTH_004",
        message="无效的认证凭证",
        status_code=401
    )

    TOKEN_REUSE_DETECTED = APIError(
        code="AUTH_005",
        message="检测到异常登录，请重新登录",
        status_code=401
    )

    PERMISSION_DENIED = APIError(
        code="AUTH_006",
        message="权限不足",
        status_code=403
    )

    COMPANY_NOT_VERIFIED = APIError(
        code="AUTH_007",
        message="企业账号待审核",
        status_code=403
    )

    ACCOUNT_PENDING = APIError(
        code="AUTH_008",
        message="账号待审核",
        status_code=403
    )

    USERNAME_EXISTS = APIError(
        code="AUTH_009",
        message="用户名已存在",
        status_code=409
    )

    # 限流错误 (2xxx)
    RATE_LIMIT_EXCEEDED = APIError(
        code="RATE_001",
        message="请求过于频繁，请稍后再试",
        status_code=429
    )

    # 资源错误 (3xxx)
    NOT_FOUND = APIError(
        code="RES_001",
        message="资源不存在",
        status_code=404
    )

    ALREADY_EXISTS = APIError(
        code="RES_002",
        message="资源已存在",
        status_code=409
    )

    # 验证错误 (4xxx)
    VALIDATION_ERROR = APIError(
        code="VAL_001",
        message="数据验证失败",
        status_code=422
    )

    INVALID_PASSWORD = APIError(
        code="VAL_002",
        message="密码不符合要求",
        status_code=422
    )


def invalid_credentials() -> HTTPException:
    """无效凭证错误"""
    return APIError(
        code="AUTH_001",
        message="用户名或密码错误",
        status_code=401
    ).to_http_exception()


def account_locked(minutes: int = 15) -> HTTPException:
    """账号锁定错误"""
    return APIError(
        code="AUTH_002",
        message=f"账号已锁定，请{minutes}分钟后重试",
        status_code=423
    ).to_http_exception()


def token_expired() -> HTTPException:
    """Token过期错误"""
    return APIError(
        code="AUTH_003",
        message="登录已过期，请重新登录",
        status_code=401
    ).to_http_exception()


def token_invalid() -> HTTPException:
    """Token无效错误"""
    return APIError(
        code="AUTH_004",
        message="无效的认证凭证",
        status_code=401
    ).to_http_exception()


def token_reuse_detected() -> HTTPException:
    """Token重用检测错误"""
    return APIError(
        code="AUTH_005",
        message="检测到异常登录，请重新登录",
        status_code=401
    ).to_http_exception()


def permission_denied() -> HTTPException:
    """权限不足错误"""
    return APIError(
        code="AUTH_006",
        message="权限不足",
        status_code=403
    ).to_http_exception()


def company_not_verified() -> HTTPException:
    """企业未审核错误"""
    return APIError(
        code="AUTH_007",
        message="企业账号待审核",
        status_code=403
    ).to_http_exception()


def rate_limit_exceeded() -> HTTPException:
    """限流错误"""
    return APIError(
        code="RATE_001",
        message="请求过于频繁，请稍后再试",
        status_code=429
    ).to_http_exception()
