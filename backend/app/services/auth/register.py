"""
注册服务
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Account, Role, StudentProfile, Company, ROLE_CODES
from app.core.password import hash_password, validate_strength
from app.core.errors import APIError


class RegisterService:
    """注册服务"""

    def __init__(self, db: Session):
        self.db = db

    def _generate_account_id(self, role: str) -> str:
        """生成账户ID"""
        prefix = {
            ROLE_CODES["STUDENT"]: "STU",
            ROLE_CODES["SCHOOL_ADMIN"]: "SCH",
            ROLE_CODES["COMPANY_ADMIN"]: "CO",
            ROLE_CODES["ADMIN"]: "ADM",
        }.get(role, "USR")

        # 生成6位数字后缀
        suffix = str(int(datetime.utcnow().timestamp()))[-6:]
        return f"{prefix}{suffix}"

    def _get_role_by_code(self, role_code: str) -> Role:
        """根据角色代码获取角色"""
        role = self.db.query(Role).filter(Role.role_code == role_code).first()
        if not role:
            raise APIError(
                code="VAL_003",
                message=f"无效的角色: {role_code}",
                status_code=400
            )
        return role

    async def register(
        self,
        username: str,
        password: str,
        role: str,
        real_name: str,
        email: str = None,
        phone: str = None
    ) -> Account:
        """
        注册账户

        Args:
            username: 用户名
            password: 密码
            role: 角色代码
            real_name: 真实姓名
            email: 邮箱
            phone: 手机号

        Returns:
            Account对象
        """
        # 检查用户名是否已存在
        existing = self.db.query(Account).filter(
            Account.username == username
        ).first()
        if existing:
            raise APIError(
                code="AUTH_009",
                message="用户名已存在",
                status_code=409
            )

        # 验证密码强度
        valid, msg = validate_strength(password)
        if not valid:
            raise APIError(
                code="VAL_002",
                message=f"密码不符合要求: {msg}",
                status_code=422
            )

        # 获取角色
        role_obj = self._get_role_by_code(role)

        # 确定账户状态
        # 学生和学校管理员：自动通过
        # 企业：需要审核
        if role == ROLE_CODES["COMPANY_ADMIN"]:
            status = "pending"
        else:
            status = "active"

        # 生成账户ID
        account_id = self._generate_account_id(role)

        # 创建账户
        account = Account(
            account_id=account_id,
            username=username,
            password_hash=hash_password(password),
            real_name=real_name,
            email=email,
            phone=phone,
            status=status
        )
        account.roles.append(role_obj)

        self.db.add(account)

        # 根据角色创建对应的档案
        if role == ROLE_CODES["STUDENT"]:
            profile = StudentProfile(account_id=account_id)
            self.db.add(profile)
        elif role == ROLE_CODES["COMPANY_ADMIN"]:
            company_id = f"CO{uuid.uuid4().hex[:8].upper()}"
            company = Company(
                company_id=company_id,
                account_id=account_id,
                company_name=real_name  # 初始名称，后续可修改
            )
            self.db.add(company)

        self.db.commit()
        self.db.refresh(account)

        return account
