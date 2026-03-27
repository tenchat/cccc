"""
Token服务
"""
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from app.core import (
    decode_token,
    decode_refresh_token,
    create_access_token,
    create_refresh_token,
    get_session_manager,
    get_redis_client,
    get_redis_client,
    AuditLogger,
    AuditEvent,
    AuditContext
)
from app.core.errors import APIError
from app.models import Account


class TokenService:
    """Token服务"""

    def __init__(self, db: Session):
        self.db = db
        self.session_manager = get_session_manager()
        self.redis = get_redis_client()

    async def refresh(
        self,
        refresh_token: str,
        ip_address: str,
        user_agent: str,
        background_tasks: BackgroundTasks = None
    ) -> dict:
        """
        刷新Token

        Rotation机制：
        1. 验证refresh_token存在
        2. 检查是否已被使用过（token重用检测）
        3. 生成新tokens
        4. 删除旧refresh_token

        Args:
            refresh_token: 刷新令牌
            ip_address: IP地址
            user_agent: 用户代理

        Returns:
            新的tokens
        """
        # 解析refresh token
        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise APIError(
                code="AUTH_003",
                message="无效的refresh token",
                status_code=401
            )

        account_id = payload["sub"]
        old_jti = payload["jti"]

        # 验证token在Redis中存在
        if not self.session_manager.validate_refresh_token(account_id, old_jti):
            raise APIError(
                code="AUTH_003",
                message="refresh token已失效",
                status_code=401
            )

        # 检测token是否被重复使用（泄露检测）
        if self.session_manager.is_token_used(account_id, old_jti):
            # Token重用！可能遭到攻击
            # 吊销该用户所有会话
            self.session_manager.revoke_all_sessions(account_id)

            # 记录审计日志
            audit = AuditLogger(self.db)
            if background_tasks:
                background_tasks.add_task(
                    audit.log_token_reuse,
                    account_id, ip_address
                )
            else:
                await audit.log_token_reuse(account_id, ip_address)

            raise APIError(
                code="AUTH_005",
                message="检测到异常登录，请重新登录",
                status_code=401
            )

        # 获取账户信息
        account = self.db.query(Account).filter(
            Account.account_id == account_id
        ).first()

        if not account:
            raise APIError(
                code="AUTH_001",
                message="用户不存在",
                status_code=401
            )

        # 标记旧token为已使用
        self.session_manager.mark_token_used(account_id, old_jti)

        # 删除旧refresh token
        self.session_manager.delete_refresh_token(account_id, old_jti)

        # 生成新tokens
        role = account.role if account.roles else ""
        new_access_token, new_access_jti = create_access_token(
            account_id,
            role,
            self.redis.redis.get("secret_key") or "default-secret"
        )
        new_refresh_token, new_refresh_jti = create_refresh_token(
            account_id,
            self.redis.redis.get("secret_key") or "default-secret"
        )

        # 存储新refresh token
        self.session_manager.store_refresh_token(
            account_id=account_id,
            refresh_jti=new_refresh_jti,
            access_jti=new_access_jti,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 记录审计日志
        audit = AuditLogger(self.db)
        if background_tasks:
            background_tasks.add_task(
                audit.log, AuditEvent.TOKEN_REFRESH,
                AuditContext(
                    account_id=account_id,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": 3600
        }

    async def logout(
        self,
        access_token: str,
        refresh_token: str,
        account_id: str,
        ip_address: str,
        user_agent: str,
        background_tasks: BackgroundTasks = None
    ):
        """
        登出

        Args:
            access_token: 访问令牌
            refresh_token: 刷新令牌
            account_id: 账户ID
            ip_address: IP地址
            user_agent: 用户代理
        """
        # 解析access token获取jti
        payload = decode_token(access_token)
        if payload:
            # 将access token加入黑名单
            self.session_manager.add_to_blacklist(payload.jti, 3600)  # TTL=1小时

        # 删除refresh token
        refresh_payload = decode_refresh_token(refresh_token)
        if refresh_payload:
            self.session_manager.delete_refresh_token(
                account_id,
                refresh_payload["jti"]
            )

        # 记录审计日志
        audit = AuditLogger(self.db)
        if background_tasks:
            background_tasks.add_task(
                audit.log, AuditEvent.LOGOUT,
                AuditContext(
                    account_id=account_id,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            )
