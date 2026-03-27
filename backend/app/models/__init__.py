"""
Models模块 - 数据模型层
"""
from app.models.base import Base
from app.models.account import Account, AccountStatus
from app.models.role import Role, Permission, account_roles, role_permissions, ROLE_CODES
from app.models.session import Session
from app.models.audit_log import AuditLog
from app.models.student import StudentProfile
from app.models.company import Company
from app.models.school import University, SchoolAdmin
from app.models.job import JobDescription, JobApplication

__all__ = [
    "Base",
    # account
    "Account",
    "AccountStatus",
    # role
    "Role",
    "Permission",
    "account_roles",
    "role_permissions",
    "ROLE_CODES",
    # session
    "Session",
    # audit
    "AuditLog",
    # student
    "StudentProfile",
    # company
    "Company",
    # school
    "University",
    "SchoolAdmin",
    # job
    "JobDescription",
    "JobApplication",
]
