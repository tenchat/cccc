"""
JWT服务模块
职责：Token创建、解析、黑名单检查
"""
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import jwt, JWTError
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """JWT Payload结构"""
    sub: str          # account_id
    jti: str         # token唯一ID
    exp: datetime     # 过期时间
    role: str         # 角色


def create_access_token(
    account_id: str,
    role: str,
    secret_key: str,
    expires_delta: timedelta = timedelta(hours=1)
) -> Tuple[str, str]:
    """
    创建访问令牌

    Returns:
        (token, jti)
    """
    jti = str(uuid.uuid4())
    exp = datetime.utcnow() + expires_delta

    payload = {
        "sub": account_id,
        "jti": jti,
        "exp": exp,
        "role": role,
        "type": "access"
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token, jti


def create_refresh_token(
    account_id: str,
    secret_key: str,
    expires_delta: timedelta = timedelta(days=7)
) -> Tuple[str, str]:
    """
    创建刷新令牌

    Returns:
        (token, jti)
    """
    jti = str(uuid.uuid4())
    exp = datetime.utcnow() + expires_delta

    payload = {
        "sub": account_id,
        "jti": jti,
        "exp": exp,
        "type": "refresh"
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token, jti


def decode_token(token: str, secret_key: str) -> Optional[TokenPayload]:
    """
    解析令牌

    Returns:
        TokenPayload或None（解析失败时）
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return TokenPayload(
            sub=payload["sub"],
            jti=payload["jti"],
            exp=datetime.fromtimestamp(payload["exp"]),
            role=payload.get("role", "")
        )
    except JWTError:
        return None


def decode_refresh_token(token: str, secret_key: str) -> Optional[dict]:
    """
    解析刷新令牌（不验证角色）

    Returns:
        dict或None
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None


def get_token_fingerprint(token: str) -> str:
    """获取Token指纹"""
    return hashlib.sha256(token.encode()).hexdigest()
