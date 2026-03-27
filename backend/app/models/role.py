"""
角色和权限模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.models.base import Base


# 关联表
account_roles = Table(
    'account_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('account_id', String(20), ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow)
)


class Role(Base):
    """角色模型"""
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_code = Column(String(20), unique=True, nullable=False)
    role_name = Column(String(50), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    accounts = relationship("Account", secondary=account_roles, back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    """权限模型"""
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    permission_code = Column(String(50), unique=True, nullable=False)
    permission_name = Column(String(50), nullable=False)
    resource_type = Column(String(20))  # user, job, report, college, scarce, ai
    action = Column(String(20))  # read, write, delete, export
    description = Column(String(255))

    # 关系
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permissions.permission_id', ondelete='CASCADE'), nullable=False)
)


# 预定义角色
ROLE_CODES = {
    "STUDENT": "student",
    "SCHOOL_ADMIN": "school_admin",
    "COMPANY_ADMIN": "company_admin",
    "ADMIN": "admin"
}
