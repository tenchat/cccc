"""
FastAPI依赖注入模块
"""
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core import (
    get_redis_client,
    decode_token,
    is_account_locked,
    get_session_manager,
    RedisClient,
    SessionManager,
    AuditLogger,
    AuditEvent,
    AuditContext
)
from app.models.account import Account


security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> Account:
    """
    获取当前登录用户

    检查流程：
    1. 解析JWT token
    2. 检查是否在黑名单
    3. 检查账号是否被锁定
    4. 从数据库加载用户信息
    5. 检查账号状态
    """
    token = credentials.credentials

    # 1. 解析token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )

    # 2. 检查黑名单
    redis = get_redis_client()
    if redis.exists(f"blacklist:{payload.jti}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证凭证已失效"
        )

    # 3. 检查账号锁定
    if is_account_locked(payload.sub):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="账号已锁定，请15分钟后重试"
        )

    # 4. 加载用户
    account = db.query(Account).filter(
        Account.account_id == payload.sub
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    # 5. 检查账号状态
    if account.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号状态异常，请联系管理员"
        )

    return account


def require_roles(*allowed_roles: str):
    """
    角色检查依赖

    用法:
    @router.post("/jobs", dependencies=[require_roles("company_admin")])
    @router.get("/students", dependencies=[require_roles("school_admin")])
    """
    async def checker(current_user: Account = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        return current_user
    return checker


def get_audit_context(request: Request, account: Account = None) -> AuditContext:
    """从请求中构建审计上下文"""
    return AuditContext(
        account_id=account.account_id if account else None,
        username=account.username if account else None,
        ip_address=request.client.host if request.client else None,
        user_agent=str(request.headers.get("user-agent", "")),
        request_id=getattr(request.state, "request_id", None)
    )


def get_session_manager_dep() -> SessionManager:
    """获取会话管理器"""
    return get_session_manager()


def get_audit_logger(db: Session = Depends(get_db)) -> AuditLogger:
    """获取审计日志器"""
    return AuditLogger(db)
