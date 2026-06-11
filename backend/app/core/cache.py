"""
=========================================================
Pageless Gradient
Enterprise Redis Cache Service
=========================================================

Features
--------
✓ Namespaced Keys
✓ JSON Serialization
✓ Automatic Compression
✓ Cache Aside Pattern
✓ TTL Support
✓ Bulk Operations
✓ Hash Operations
✓ Set Operations
✓ List Operations
✓ Counter Operations
✓ Distributed Locks
✓ Pattern Invalidation
✓ Namespace Cleanup
✓ Metrics
✓ Health Checks
✓ Graceful Error Handling
✓ Async Native

Used By
--------
- Authentication
- User Sessions
- Topics
- Sessions
- Blocks
- Sharing
- AI Responses
- Analytics
- Rate Limiting

=========================================================
"""

from __future__ import annotations

import base64
import gzip
import json
import logging
from typing import Any
from typing import Awaitable
from typing import Callable

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


# =========================================================
# Metrics
# =========================================================

class CacheMetrics:

    def __init__(self):
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses

        if total == 0:
            return 0.0

        return round(
            (self.hits / total) * 100,
            2,
        )

    def as_dict(self):
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hit_rate,
        }


# =========================================================
# Cache Service
# =========================================================

class CacheService:

    DEFAULT_TTL = 3600

    COMPRESSION_THRESHOLD = 2048

    def __init__(
        self,
        redis_client: Redis,
        namespace: str = "gradient:v1",
    ):
        self.redis = redis_client
        self.namespace = namespace
        self.metrics = CacheMetrics()

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def _serialize(self, value: Any) -> str:

        payload = json.dumps(
            value,
            default=str,
            ensure_ascii=False,
        )

        if len(payload) < self.COMPRESSION_THRESHOLD:
            return payload

        compressed = gzip.compress(
            payload.encode("utf-8")
        )

        encoded = base64.b64encode(
            compressed
        ).decode()

        return f"__gz__:{encoded}"

    def _deserialize(
        self,
        value: str | None,
    ) -> Any:

        if value is None:
            return None

        try:

            if (
                isinstance(value, str)
                and value.startswith("__gz__:")
            ):

                encoded = value[7:]

                compressed = (
                    base64.b64decode(encoded)
                )

                decompressed = gzip.decompress(
                    compressed
                ).decode()

                return json.loads(
                    decompressed
                )

            return json.loads(value)

        except Exception:
            return value

    # =====================================================
    # Basic Cache
    # =====================================================

    async def get(
        self,
        key: str,
    ) -> Any:

        try:

            value = await self.redis.get(
                self._key(key)
            )

            if value is None:
                self.metrics.record_miss()
                return None

            self.metrics.record_hit()

            return self._deserialize(value)

        except Exception as exc:

            logger.exception(
                "Redis GET failed: %s",
                exc,
            )

            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:

        try:

            return await self.redis.set(
                self._key(key),
                self._serialize(value),
                ex=ttl or self.DEFAULT_TTL,
            )

        except Exception as exc:

            logger.exception(
                "Redis SET failed: %s",
                exc,
            )

            return False

    async def delete(
        self,
        key: str,
    ) -> int:

        return await self.redis.delete(
            self._key(key)
        )

    async def exists(
        self,
        key: str,
    ) -> bool:

        return bool(
            await self.redis.exists(
                self._key(key)
            )
        )

    async def ttl(
        self,
        key: str,
    ) -> int:

        return await self.redis.ttl(
            self._key(key)
        )

    async def expire(
        self,
        key: str,
        ttl: int,
    ):

        return await self.redis.expire(
            self._key(key),
            ttl,
        )

    # =====================================================
    # Cache Aside Pattern
    # =====================================================

    async def remember(
        self,
        key: str,
        loader: Callable[
            [],
            Awaitable[Any],
        ],
        ttl: int | None = None,
    ):

        cached = await self.get(key)

        if cached is not None:
            return cached

        value = await loader()

        await self.set(
            key,
            value,
            ttl,
        )

        return value

    # =====================================================
    # Bulk Operations
    # =====================================================

    async def mget(
        self,
        keys: list[str],
    ) -> list[Any]:

        values = await self.redis.mget(
            [
                self._key(k)
                for k in keys
            ]
        )

        return [
            self._deserialize(v)
            for v in values
        ]

    async def mset(
        self,
        values: dict[str, Any],
        ttl: int | None = None,
    ):

        pipe = self.redis.pipeline()

        for key, value in values.items():

            pipe.set(
                self._key(key),
                self._serialize(value),
                ex=ttl,
            )

        await pipe.execute()

    async def mdelete(
        self,
        keys: list[str],
    ):

        redis_keys = [
            self._key(k)
            for k in keys
        ]

        if redis_keys:
            await self.redis.delete(
                *redis_keys
            )

    # =====================================================
    # Hash Operations
    # =====================================================

    async def hset(
        self,
        name: str,
        field: str,
        value: Any,
    ):

        await self.redis.hset(
            self._key(name),
            field,
            self._serialize(value),
        )

    async def hget(
        self,
        name: str,
        field: str,
    ):

        value = await self.redis.hget(
            self._key(name),
            field,
        )

        return self._deserialize(value)

    async def hgetall(
        self,
        name: str,
    ):

        data = await self.redis.hgetall(
            self._key(name)
        )

        return {
            k: self._deserialize(v)
            for k, v in data.items()
        }

    # =====================================================
    # Set Operations
    # =====================================================

    async def sadd(
        self,
        key: str,
        *values: str,
    ):

        return await self.redis.sadd(
            self._key(key),
            *values,
        )

    async def smembers(
        self,
        key: str,
    ):

        return await self.redis.smembers(
            self._key(key)
        )

    # =====================================================
    # List Operations
    # =====================================================

    async def lpush(
        self,
        key: str,
        value: Any,
    ):

        await self.redis.lpush(
            self._key(key),
            self._serialize(value),
        )

    async def rpush(
        self,
        key: str,
        value: Any,
    ):

        await self.redis.rpush(
            self._key(key),
            self._serialize(value),
        )

    async def lrange(
        self,
        key: str,
        start: int = 0,
        end: int = -1,
    ):

        values = await self.redis.lrange(
            self._key(key),
            start,
            end,
        )

        return [
            self._deserialize(v)
            for v in values
        ]

    # =====================================================
    # Counters
    # =====================================================

    async def increment(
        self,
        key: str,
        amount: int = 1,
    ):

        return await self.redis.incrby(
            self._key(key),
            amount,
        )

    async def decrement(
        self,
        key: str,
        amount: int = 1,
    ):

        return await self.redis.decrby(
            self._key(key),
            amount,
        )

    # =====================================================
    # Distributed Locks
    # =====================================================

    async def acquire_lock(
        self,
        key: str,
        ttl: int = 30,
    ) -> bool:

        return await self.redis.set(
            self._key(f"lock:{key}"),
            "1",
            ex=ttl,
            nx=True,
        )

    async def release_lock(
        self,
        key: str,
    ):

        await self.delete(
            f"lock:{key}"
        )

    # =====================================================
    # Pattern Invalidation
    # =====================================================

    async def invalidate_pattern(
        self,
        pattern: str,
    ):

        cursor = 0

        match_pattern = (
            f"{self.namespace}:{pattern}"
        )

        while True:

            cursor, keys = (
                await self.redis.scan(
                    cursor=cursor,
                    match=match_pattern,
                    count=100,
                )
            )

            if keys:
                await self.redis.delete(
                    *keys
                )

            if cursor == 0:
                break

    # =====================================================
    # Namespace Cleanup
    # =====================================================

    async def clear_namespace(
        self,
    ):

        await self.invalidate_pattern("*")

    # =====================================================
    # Metrics
    # =====================================================

    def stats(self):

        return self.metrics.as_dict()

    # =====================================================
    # Health Check
    # =====================================================

    async def health(self):

        try:

            pong = await self.redis.ping()

            return {
                "status": "healthy",
                "ping": pong,
                "namespace": self.namespace,
                "metrics": self.stats(),
            }

        except Exception as exc:

            return {
                "status": "unhealthy",
                "error": str(exc),
            }

    async def ping(self) -> bool:

        try:
            return await self.redis.ping()

        except Exception:
            return False