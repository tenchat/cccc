"""
会话模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Session(Base):
    """会话模型"""
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)  # UUID
    account_id = Column(String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    jti = Column(String(36), unique=True, nullable=False, index=True)  # JWT ID
    refresh_jti = Column(String(36), unique=True, nullable=True)  # Refresh Token JTI

    device_info = Column(String(255))  # 设备信息
    ip_address = Column(String(50))
    user_agent = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    # Token指纹（用于泄露检测）
    token_fingerprint = Column(String(64))

    is_active = Column(Boolean, default=True)

    # 关系
    account = relationship("Account", back_populates="sessions")

    def to_dict(self, current_session_id: str = None) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "is_current": self.id == current_session_id
        }
