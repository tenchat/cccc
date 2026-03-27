"""
Core模块 - 基础设施层
"""
from .password import hash_password, verify_password, validate_strength
from .jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    decode_refresh_token,
    get_token_fingerprint,
    TokenPayload
)
from .redis_client import get_redis_client, RedisClient
from .rate_limiter import get_rate_limiter, RateLimiter
from .lockout import (
    is_account_locked,
    record_failed_attempt,
    clear_failed_attempts,
    force_unlock,
    AccountLockout
)
from .session import get_session_manager, SessionManager
from .audit import AuditLogger, AuditEvent, AuditContext, AuditSeverity
from .errors import (
    APIError,
    Errors,
    invalid_credentials,
    account_locked,
    token_expired,
    token_invalid,
    token_reuse_detected,
    permission_denied,
    company_not_verified,
    rate_limit_exceeded
)

__all__ = [
    # password
    "hash_password",
    "verify_password",
    "validate_strength",
    # jwt
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "decode_refresh_token",
    "get_token_fingerprint",
    "TokenPayload",
    # redis
    "get_redis_client",
    "RedisClient",
    # rate_limiter
    "get_rate_limiter",
    "RateLimiter",
    # lockout
    "is_account_locked",
    "record_failed_attempt",
    "clear_failed_attempts",
    "force_unlock",
    "AccountLockout",
    # session
    "get_session_manager",
    "SessionManager",
    # audit
    "AuditLogger",
    "AuditEvent",
    "AuditContext",
    "AuditSeverity",
    # errors
    "APIError",
    "Errors",
    "invalid_credentials",
    "account_locked",
    "token_expired",
    "token_invalid",
    "token_reuse_detected",
    "permission_denied",
    "company_not_verified",
    "rate_limit_exceeded",
]
