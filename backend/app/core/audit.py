"""
审计日志模块
职责：关键事件同步写入，普通事件异步写入
"""
import json
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from dataclasses import dataclass, asdict

from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from core.redis_client import get_redis_client


class AuditSeverity(str, Enum):
    """审计日志严重级别"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AuditEvent(str, Enum):
    """审计事件类型"""
    # 认证相关
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    LOGOUT = "LOGOUT"
    TOKEN_REFRESH = "TOKEN_REFRESH"
    TOKEN_REUSE_DETECTED = "TOKEN_REUSE_DETECTED"
    SESSION_REVOKED = "SESSION_REVOKED"
    ALL_SESSIONS_REVOKED = "ALL_SESSIONS_REVOKED"

    # 账号相关
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_UNLOCKED = "ACCOUNT_UNLOCKED"
    ACCOUNT_CREATED = "ACCOUNT_CREATED"
    ACCOUNT_STATUS_CHANGED = "ACCOUNT_STATUS_CHANGED"

    # 业务相关
    PROFILE_UPDATE = "PROFILE_UPDATE"
    JOB_PUBLISH = "JOB_PUBLISH"
    JOB_APPLY = "JOB_APPLY"
    JOB_WITHDRAW = "JOB_WITHDRAW"

    # 安全相关
    CROSS_SCHOOL_ACCESS = "CROSS_SCHOOL_ACCESS"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    ADMIN_ACTION = "ADMIN_ACTION"

    # 企业相关
    COMPANY_REGISTERED = "COMPANY_REGISTERED"
    COMPANY_VERIFIED = "COMPANY_VERIFIED"
    COMPANY_REJECTED = "COMPANY_REJECTED"


# 关键事件（同步写入）
CRITICAL_EVENTS = {
    AuditEvent.LOGIN_FAILED,
    AuditEvent.TOKEN_REUSE_DETECTED,
    AuditEvent.ACCOUNT_LOCKED,
    AuditEvent.CROSS_SCHOOL_ACCESS,
    AuditEvent.UNAUTHORIZED_ACCESS,
    AuditEvent.ADMIN_ACTION,
}


@dataclass
class AuditContext:
    """审计上下文"""
    account_id: Optional[str] = None
    username: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    result: Optional[str] = None
    details: Optional[dict] = None


class AuditLogger:
    """审计日志记录器"""

    def __init__(self, db: Session):
        self.db = db
        self.redis = get_redis_client()

    def _build_log_entry(
        self,
        event: AuditEvent,
        context: AuditContext,
        severity: AuditSeverity
    ) -> dict:
        """构建日志条目"""
        return {
            "timestamp": datetime.utcnow(),
            "event": event.value,
            "severity": severity.value,
            "account_id": context.account_id,
            "username": context.username,
            "ip_address": context.ip_address,
            "user_agent": context.user_agent,
            "session_id": context.session_id,
            "resource": context.resource,
            "action": context.action,
            "result": context.result,
            "details": json.dumps(context.details) if context.details else None,
            "request_id": context.request_id
        }

    async def log(
        self,
        event: AuditEvent,
        context: AuditContext,
        background_tasks: Optional[BackgroundTasks] = None
    ):
        """
        记录审计日志

        Args:
            event: 事件类型
            context: 审计上下文
            background_tasks: FastAPI BackgroundTasks（用于异步写入）
        """
        # 判断严重级别
        severity = AuditSeverity.CRITICAL if event in CRITICAL_EVENTS else AuditSeverity.INFO
        if event in {AuditEvent.LOGIN_FAILED, AuditEvent.ACCOUNT_LOCKED}:
            severity = AuditSeverity.WARNING

        log_entry = self._build_log_entry(event, context, severity)

        if event in CRITICAL_EVENTS:
            # 关键事件：同步写入
            await self._sync_write(log_entry)
            # 备份到Redis队列
            await self._queue_backup(log_entry)
        else:
            # 普通事件：异步写入
            if background_tasks:
                background_tasks.add_task(self._async_write, log_entry)
            else:
                await self._async_write(log_entry)

    async def _sync_write(self, log_entry: dict):
        """同步写入数据库（关键事件）"""
        try:
            from app.models.audit_log import AuditLog
            audit_record = AuditLog(**log_entry)
            self.db.add(audit_record)
            self.db.commit()
        except Exception as e:
            # 同步写入失败，仍尝试备份
            await self._queue_backup(log_entry)

    async def _async_write(self, log_entry: dict):
        """异步写入数据库（普通事件）"""
        try:
            from app.models.audit_log import AuditLog
            audit_record = AuditLog(**log_entry)
            self.db.add(audit_record)
            self.db.commit()
        except Exception:
            # 异步写入失败，尝试备份
            await self._queue_backup(log_entry)

    async def _queue_backup(self, log_entry: dict):
        """Redis队列备份（防止DB写入失败）"""
        try:
            self.redis.rpush("audit:backup", json.dumps(log_entry, default=str))
        except Exception:
            pass  # 备份也失败，忽略

    async def log_login_success(
        self,
        account_id: str,
        username: str,
        ip_address: str,
        user_agent: str,
        background_tasks: BackgroundTasks = None
    ):
        """记录登录成功"""
        context = AuditContext(
            account_id=account_id,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            result="SUCCESS"
        )
        await self.log(AuditEvent.LOGIN_SUCCESS, context, background_tasks)

    async def log_login_failed(
        self,
        username: str,
        ip_address: str,
        user_agent: str,
        reason: str,
        background_tasks: BackgroundTasks = None
    ):
        """记录登录失败"""
        context = AuditContext(
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            result="FAILURE",
            details={"reason": reason}
        )
        await self.log(AuditEvent.LOGIN_FAILED, context, background_tasks)

    async def log_token_reuse(
        self,
        account_id: str,
        ip_address: str,
        background_tasks: BackgroundTasks = None
    ):
        """记录Token重用检测"""
        context = AuditContext(
            account_id=account_id,
            ip_address=ip_address,
            result="BLOCKED",
            details={"action": "强制重新登录"}
        )
        await self.log(AuditEvent.TOKEN_REUSE_DETECTED, context, background_tasks)
