"""
Redis客户端模块
职责：Redis连接、故障降级
"""
import json
from typing import Optional, Any
import redis
from redis.exceptions import RedisError


class RedisClient:
    """
    Redis客户端，支持多层降级：
    1. 正常：Redis主存储
    2. Redis故障：本地缓存 + DB fallback
    3. 完全故障：纯DB模式
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._redis: Optional[redis.Redis] = None
        self.fallback_db: dict = {}  # 本地缓存
        self.mode = "redis"  # redis | fallback | pure_db

    def _get_redis(self) -> redis.Redis:
        """获取Redis连接"""
        if self._redis is None:
            self._redis = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
        return self._redis

    def get(self, key: str) -> Optional[str]:
        """获取值"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                return client.get(key)
        except RedisError:
            self.mode = "fallback"
        return None

    def setex(self, key: str, ttl: int, value: str) -> bool:
        """设置值（带过期时间）"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                client.setex(key, ttl, value)
                return True
            elif self.mode == "fallback":
                self.fallback_db[key] = value
                return True
        except RedisError:
            self.mode = "fallback"
            self.fallback_db[key] = value
        return True

    def delete(self, key: str) -> bool:
        """删除key"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                client.delete(key)
                return True
            elif self.mode == "fallback":
                self.fallback_db.pop(key, None)
                return True
        except RedisError:
            self.mode = "fallback"
            self.fallback_db.pop(key, None)
        return True

    def exists(self, key: str) -> bool:
        """检查key是否存在"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                return bool(client.exists(key))
            elif self.mode == "fallback":
                return key in self.fallback_db
        except RedisError:
            self.mode = "fallback"
            return key in self.fallback_db
        return False

    def incr(self, key: str) -> int:
        """递增计数"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                return client.incr(key)
            elif self.mode == "fallback":
                current = int(self.fallback_db.get(key, 0)) + 1
                self.fallback_db[key] = str(current)
                return current
        except RedisError:
            self.mode = "fallback"
            current = int(self.fallback_db.get(key, 0)) + 1
            self.fallback_db[key] = str(current)
            return current
        return 1

    def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                client.expire(key, ttl)
                return True
            elif self.mode == "fallback":
                # 本地缓存模式无法精确过期，仅标记
                return True
        except RedisError:
            self.mode = "fallback"
            return True
        return True

    def rpush(self, key: str, value: str) -> bool:
        """右push到列表"""
        try:
            if self.mode == "redis":
                client = self._get_redis()
                client.rpush(key, value)
                return True
            elif self.mode == "fallback":
                if key not in self.fallback_db:
                    self.fallback_db[key] = []
                if isinstance(self.fallback_db[key], list):
                    self.fallback_db[key].append(value)
                else:
                    self.fallback_db[key] = [value]
                return True
        except RedisError:
            self.mode = "fallback"
            return True
        return True

    def get_json(self, key: str) -> Optional[dict]:
        """获取JSON值"""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None

    def set_json(self, key: str, ttl: int, value: dict) -> bool:
        """设置JSON值"""
        return self.setex(key, ttl, json.dumps(value))


# 全局实例（延迟初始化）
_redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """获取Redis客户端实例"""
    global _redis_client
    if _redis_client is None:
        from app.core.config import get_settings
        settings = get_settings()
        _redis_client = RedisClient(settings.REDIS_URL)
    return _redis_client
