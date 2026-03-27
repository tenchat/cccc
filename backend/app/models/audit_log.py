"""
审计日志模型
"""
from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, Text

from app.models.base import Base


class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    event = Column(String(50), nullable=False, index=True)
    severity = Column(String(10), nullable=False)  # INFO, WARNING, CRITICAL

    account_id = Column(String(20), index=True)
    username = Column(String(50))  # 反查用，不做外键
    ip_address = Column(String(50), index=True)
    user_agent = Column(Text)
    session_id = Column(String(36))

    resource = Column(String(50))  # 操作的资源类型
    action = Column(String(50))  # 具体动作
    result = Column(String(20))  # SUCCESS, FAILURE

    details = Column(Text)  # JSON字符串
    request_id = Column(String(36))  # 请求追踪ID
