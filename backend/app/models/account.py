"""
账户模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import Base


class AccountStatus:
    """账户状态"""
    PENDING = "pending"           # 注册待审核(企业)
    ACTIVE = "active"            # 正常
    LOCKED = "locked"           # 被锁定
    SUSPENDED = "suspended"      # 被禁用


class Account(Base):
    """账户模型"""
    __tablename__ = "accounts"

    account_id = Column(String(20), primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(50), nullable=False)
    email = Column(String(100), index=True)
    phone = Column(String(20), index=True)
    status = Column(String(20), default=AccountStatus.PENDING.value)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    roles = relationship("Role", secondary="account_roles", back_populates="accounts")
    sessions = relationship("Session", back_populates="account", cascade="all, delete-orphan")
    student_profile = relationship("StudentProfile", back_populates="account", uselist=False)
    company = relationship("Company", back_populates="account", uselist=False)
    school_admin = relationship("SchoolAdmin", back_populates="account", uselist=False)

    @property
    def is_active(self) -> bool:
        return self.status == AccountStatus.ACTIVE

    @property
    def is_locked(self) -> bool:
        return self.status == AccountStatus.LOCKED or (
            self.locked_until and self.locked_until > datetime.utcnow()
        )

    @property
    def role(self) -> str:
        """获取主角色"""
        if self.roles:
            return self.roles[0].role_code if self.roles else ""
        return ""
