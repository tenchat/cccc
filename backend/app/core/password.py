"""
密码服务模块
职责：密码哈希、校验、强度验证
"""
import re
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """密码哈希"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """密码校验"""
    return pwd_context.verify(plain, hashed)


def validate_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度

    Returns:
        (是否通过, 错误信息)
    """
    if len(password) < 8:
        return False, "密码至少8位"

    if len(password) > 32:
        return False, "密码最多32位"

    if not re.search(r"[A-Z]", password):
        return False, "密码必须包含大写字母"

    if not re.search(r"[a-z]", password):
        return False, "密码必须包含小写字母"

    if not re.search(r"[0-9]", password):
        return False, "密码必须包含数字"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "密码必须包含特殊字符(!@#$%^&*等)"

    return True, ""
