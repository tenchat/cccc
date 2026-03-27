"""
账号锁定模块
职责：账号锁定/解锁/检查
"""
from datetime import datetime, timedelta
from core.redis_client import get_redis_client


# 配置
LOCK_DURATION = 15 * 60       # 锁定时长（秒）
MAX_FAILED_ATTEMPTS = 5       # 最大失败次数


def is_account_locked(account_id: str) -> bool:
    """检查账号是否被锁定"""
    redis = get_redis_client()
    key = f"lock:{account_id}"
    return redis.exists(key)


def get_lock_remaining_seconds(account_id: str) -> int:
    """获取锁定剩余秒数"""
    redis = get_redis_client()
    ttl = redis.redis.ttl(f"lock:{account_id}") if redis.mode == "redis" else None
    if ttl and ttl > 0:
        return ttl
    return 0


def record_failed_attempt(account_id: str) -> int:
    """
    记录失败尝试

    Returns:
        当前失败次数
    """
    redis = get_redis_client()

    # 如果已经锁定，直接返回
    if is_account_locked(account_id):
        return MAX_FAILED_ATTEMPTS

    key = f"failed:{account_id}"
    count = redis.incr(key)

    # 首次失败，设置过期时间
    if count == 1:
        redis.expire(key, LOCK_DURATION)

    # 达到锁定阈值
    if count >= MAX_FAILED_ATTEMPTS:
        lock_key = f"lock:{account_id}"
        redis.setex(lock_key, LOCK_DURATION, "1")
        # 清除失败计数
        redis.delete(key)
        return MAX_FAILED_ATTEMPTS

    return count


def get_failed_attempts(account_id: str) -> int:
    """获取连续失败次数"""
    redis = get_redis_client()
    key = f"failed:{account_id}"
    value = redis.get(key)
    return int(value) if value else 0


def clear_failed_attempts(account_id: str):
    """清除失败记录（登录成功时调用）"""
    redis = get_redis_client()
    redis.delete(f"failed:{account_id}")


def force_unlock(account_id: str):
    """强制解锁（管理员操作）"""
    redis = get_redis_client()
    redis.delete(f"lock:{account_id}")
    redis.delete(f"failed:{account_id}")


class AccountLockout:
    """账号锁定服务"""

    def __init__(self):
        self.redis = get_redis_client()

    def is_locked(self, account_id: str) -> bool:
        """检查是否锁定"""
        return is_account_locked(account_id)

    def check_and_raise(self, account_id: str):
        """检查并抛出异常"""
        if self.is_locked(account_id):
            remaining = get_lock_remaining_seconds(account_id)
            raise PermissionError(
                f"账号已锁定，请在 {remaining // 60 + 1} 分钟后重试"
            )

    def record_failure(self, account_id: str) -> dict:
        """
        记录失败尝试

        Returns:
            {"locked": bool, "attempts": int, "remaining": int}
        """
        attempts = record_failed_attempt(account_id)
        locked = is_account_locked(account_id)

        return {
            "locked": locked,
            "attempts": attempts,
            "remaining": MAX_FAILED_ATTEMPTS - attempts if not locked else 0
        }

    def clear_failures(self, account_id: str):
        """清除失败记录"""
        clear_failed_attempts(account_id)

    def unlock(self, account_id: str):
        """解锁账号"""
        force_unlock(account_id)
