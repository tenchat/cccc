"""
限流器模块
职责：多维度请求限流
"""
from fastapi import HTTPException
from core.redis_client import get_redis_client


class RateLimiter:
    """限流器"""

    # 默认配置
    DEFAULT_IP_LIMIT = 60        # IP每分钟最多60次
    DEFAULT_USER_LIMIT = 100     # 用户每分钟最多100次
    DEFAULT_WINDOW = 60          # 时间窗口60秒

    def __init__(self):
        self.redis = get_redis_client()

    async def check_ip(self, ip: str, max_requests: int = None, window: int = None) -> bool:
        """
        IP维度限流检查

        Args:
            ip: IP地址
            max_requests: 最大请求数
            window: 时间窗口(秒)

        Returns:
            是否允许请求
        """
        max_requests = max_requests or self.DEFAULT_IP_LIMIT
        window = window or self.DEFAULT_WINDOW
        key = f"rate_limit:ip:{ip}"

        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, window)

        return count <= max_requests

    async def check_user(self, username: str, max_requests: int = None, window: int = None) -> bool:
        """
        用户名维度限流检查

        Args:
            username: 用户名
            max_requests: 最大请求数
            window: 时间窗口(秒)

        Returns:
            是否允许请求
        """
        max_requests = max_requests or self.DEFAULT_USER_LIMIT
        window = window or self.DEFAULT_WINDOW
        key = f"rate_limit:user:{username}"

        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, window)

        return count <= max_requests

    async def check_login(self, ip: str, username: str) -> bool:
        """
        登录限流检查（更严格）

        Args:
            ip: IP地址
            username: 用户名

        Returns:
            是否允许请求
        """
        # IP限制：每分钟5次
        ip_key = f"rate_limit:login:ip:{ip}"
        ip_count = self.redis.incr(ip_key)
        if ip_count == 1:
            self.redis.expire(ip_key, 60)

        if ip_count > 5:
            return False

        # 用户限制：每分钟10次
        user_key = f"rate_limit:login:user:{username}"
        user_count = self.redis.incr(user_key)
        if user_count == 1:
            self.redis.expire(user_key, 60)

        return user_count <= 10

    async def check_and_raise_ip(self, ip: str):
        """IP限流检查，超限抛异常"""
        if not await self.check_ip(ip):
            raise HTTPException(
                status_code=429,
                detail="请求过于频繁，请稍后再试"
            )

    async def check_and_raise_user(self, username: str):
        """用户限流检查，超限抛异常"""
        if not await self.check_user(username):
            raise HTTPException(
                status_code=429,
                detail="请求过于频繁，请稍后再试"
            )

    async def check_and_raise_login(self, ip: str, username: str):
        """登录限流检查，超限抛异常"""
        if not await self.check_login(ip, username):
            raise HTTPException(
                status_code=429,
                detail="登录尝试过于频繁，请稍后再试"
            )


# 全局实例
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """获取限流器实例"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
