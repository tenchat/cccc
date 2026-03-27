"""
Session管理模块
职责：会话存储、查询、终止
"""
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass

from core.redis_client import get_redis_client


@dataclass
class SessionInfo:
    """会话信息"""
    id: str
    account_id: str
    device_info: str
    ip_address: str
    created_at: str
    last_used_at: str
    is_current: bool = False


class SessionManager:
    """会话管理器"""

    REFRESH_TTL = 7 * 24 * 3600  # 7天
    ACCESS_TTL = 3600              # 1小时

    def __init__(self):
        self.redis = get_redis_client()

    def store_refresh_token(
        self,
        account_id: str,
        refresh_jti: str,
        access_jti: str,
        ip_address: str,
        user_agent: str,
        device_info: str = None
    ) -> str:
        """
        存储Refresh Token

        Returns:
            session_id
        """
        session_id = str(uuid.uuid4())

        token_data = {
            "session_id": session_id,
            "account_id": account_id,
            "refresh_jti": refresh_jti,
            "access_jti": access_jti,
            "ip": ip_address,
            "user_agent": user_agent,
            "device": device_info or "Unknown",
            "created_at": datetime.utcnow().isoformat(),
            "fingerprint": ""  # 可后续用于泄露检测
        }

        key = f"refresh:{account_id}:{refresh_jti}"
        self.redis.setex(key, self.REFRESH_TTL, json.dumps(token_data))

        # 记录到会话索引
        index_key = f"sessions:{account_id}"
        self.redis.rpush(index_key, session_id)

        return session_id

    def get_refresh_token(self, account_id: str, refresh_jti: str) -> Optional[dict]:
        """获取Refresh Token信息"""
        key = f"refresh:{account_id}:{refresh_jti}"
        return self.redis.get_json(key)

    def validate_refresh_token(self, account_id: str, refresh_jti: str) -> bool:
        """验证Refresh Token是否存在"""
        key = f"refresh:{account_id}:{refresh_jti}"
        return self.redis.exists(key)

    def delete_refresh_token(self, account_id: str, refresh_jti: str):
        """删除Refresh Token"""
        key = f"refresh:{account_id}:{refresh_jti}"
        self.redis.delete(key)

    def mark_token_used(self, account_id: str, refresh_jti: str):
        """
        标记Token为已使用（用于Rotation检测）

        存储到 used_refresh:{account_id}:{refresh_jti} = 1
        TTL = 7天（与refresh_token相同的生命周期）
        """
        used_key = f"used_refresh:{account_id}:{refresh_jti}"
        self.redis.setex(used_key, self.REFRESH_TTL, "1")

    def is_token_used(self, account_id: str, refresh_jti: str) -> bool:
        """检查Token是否已被使用过"""
        used_key = f"used_refresh:{account_id}:{refresh_jti}"
        return self.redis.exists(used_key)

    def revoke_session(self, account_id: str, refresh_jti: str, access_jti: str):
        """吊销单个会话"""
        # 删除refresh token
        self.delete_refresh_token(account_id, refresh_jti)

        # 将access token加入黑名单
        blacklist_key = f"blacklist:{access_jti}"
        self.redis.setex(blacklist_key, self.ACCESS_TTL, "1")

    def revoke_all_sessions(self, account_id: str):
        """吊销该用户所有会话"""
        # 获取所有会话
        sessions = self.list_session_ids(account_id)

        for session_id in sessions:
            session = self.get_session_by_id(session_id)
            if session:
                self.revoke_session(
                    account_id,
                    session.get("refresh_jti", ""),
                    session.get("access_jti", "")
                )

    def list_session_ids(self, account_id: str) -> List[str]:
        """列出用户所有会话ID"""
        index_key = f"sessions:{account_id}"
        # 注意：这里需要从Redis获取，实际实现需要优化
        return []

    def get_session_by_id(self, session_id: str) -> Optional[dict]:
        """根据ID获取会话信息"""
        # 需要在Redis中建立 session_id -> token_jti 的映射
        return None

    def add_to_blacklist(self, jti: str, remaining_ttl: int):
        """将Token加入黑名单"""
        key = f"blacklist:{jti}"
        self.redis.setex(key, remaining_ttl, "1")

    def is_blacklisted(self, jti: str) -> bool:
        """检查Token是否在黑名单"""
        key = f"blacklist:{jti}"
        return self.redis.exists(key)


# 全局实例
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """获取会话管理器实例"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
