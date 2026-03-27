"""
登录服务
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from app.models import Account
from app.core import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_session_manager,
    record_failed_attempt,
    clear_failed_attempts,
    get_redis_client,
    AuditLogger,
    AuditEvent,
    AuditContext
)
from app.core.errors import APIError


class LoginService:
    """登录服务"""

    def __init__(self, db: Session):
        self.db = db
        self.session_manager = get_session_manager()
        self.redis = get_redis_client()

    async def login(
        self,
        username: str,
        password: str,
        ip_address: str,
        user_agent: str,
        background_tasks: BackgroundTasks = None
    ) -> dict:
        """
        登录

        Args:
            username: 用户名
            password: 密码
            ip_address: IP地址
            user_agent: 用户代理
            background_tasks: 后台任务

        Returns:
            包含 access_token, refresh_token, user_info 的字典
        """
        # 查询账户
        account = self.db.query(Account).filter(
            Account.username == username
        ).first()

        if not account:
            # 用户不存在，记录审计日志
            audit = AuditLogger(self.db)
            context = AuditContext(
                username=username,
                ip_address=ip_address,
                user_agent=user_agent,
                result="FAILURE",
                details={"reason": "用户不存在"}
            )
            if background_tasks:
                background_tasks.add_task(
                    audit.log_login_failed,
                    username, ip_address, user_agent, "用户不存在"
                )
            else:
                await audit.log_login_failed(username, ip_address, user_agent, "用户不存在")

            raise APIError(
                code="AUTH_001",
                message="用户名或密码错误",
                status_code=401
            )

        # 检查密码
        if not verify_password(password, account.password_hash):
            # 记录失败尝试
            lockout_info = record_failed_attempt(account.account_id)

            audit = AuditLogger(self.db)
            if background_tasks:
                background_tasks.add_task(
                    audit.log_login_failed,
                    username, ip_address, user_agent, "密码错误"
                )
            else:
                await audit.log_login_failed(username, ip_address, user_agent, "密码错误")

            if lockout_info["locked"]:
                raise APIError(
                    code="AUTH_002",
                    message=f"账号已锁定，请15分钟后重试",
                    status_code=423
                )

            raise APIError(
                code="AUTH_001",
                message="用户名或密码错误",
                status_code=401
            )

        # 检查账号状态
        if account.status == "locked":
            raise APIError(
                code="AUTH_002",
                message="账号已锁定，请联系管理员",
                status_code=423
            )

        if account.status == "pending":
            raise APIError(
                code="AUTH_008",
                message="账号待审核",
                status_code=403
            )

        if account.status != "active":
            raise APIError(
                code="AUTH_010",
                message="账号状态异常",
                status_code=403
            )

        # 清除失败记录
        clear_failed_attempts(account.account_id)

        # 获取角色
        role = account.role if account.roles else ""

        # 生成tokens
        access_token, access_jti = create_access_token(
            account.account_id,
            role,
            self.redis.redis.get("secret_key") or "default-secret"  # TODO: 从配置获取
        )
        refresh_token, refresh_jti = create_refresh_token(
            account.account_id,
            self.redis.redis.get("secret_key") or "default-secret"
        )

        # 存储会话
        self.session_manager.store_refresh_token(
            account_id=account.account_id,
            refresh_jti=refresh_jti,
            access_jti=access_jti,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 更新最后登录时间
        account.last_login_at = datetime.utcnow()
        self.db.commit()

        # 记录审计日志
        audit = AuditLogger(self.db)
        if background_tasks:
            background_tasks.add_task(
                audit.log_login_success,
                account.account_id, username, ip_address, user_agent
            )
        else:
            await audit.log_login_success(account.account_id, username, ip_address, user_agent)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "account_id": account.account_id,
                "username": account.username,
                "real_name": account.real_name,
                "role": role,
                "status": account.status,
                "email": account.email,
                "phone": account.phone
            }
        }
