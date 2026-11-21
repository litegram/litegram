from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest

from litegram.fsm.storage.memory import DisabledEventIsolation
from litegram.fsm.storage.redis import RedisEventIsolation, RedisStorage

if TYPE_CHECKING:
    from litegram.fsm.storage.base import BaseEventIsolation, StorageKey


class TestIsolations:
    @pytest.mark.asyncio
    async def test_lock(
        self,
        isolation: BaseEventIsolation,
        storage_key: StorageKey,
    ):
        async with isolation.lock(key=storage_key):
            if isinstance(isolation, DisabledEventIsolation):
                # DisabledEventIsolation should not block
                async with asyncio.timeout(1):
                    async with isolation.lock(key=storage_key):
                        pass
                return

            # Verify that we cannot acquire the lock again (non-reentrant)
            with pytest.raises((asyncio.TimeoutError, TimeoutError)):
                await asyncio.wait_for(isolation.lock(key=storage_key).__aenter__(), timeout=0.1)


class TestRedisEventIsolation:
    def test_create_isolation(self):
        fake_redis = object()
        storage = RedisStorage(redis=fake_redis)
        isolation = storage.create_isolation()
        assert isinstance(isolation, RedisEventIsolation)
        assert isolation.redis is fake_redis
        assert isolation.key_builder is storage.key_builder

    def test_init_without_key_builder(self):
        redis = AsyncMock()
        isolation = RedisEventIsolation(redis=redis)
        assert isolation.redis is redis

        assert isolation.key_builder is not None

    def test_init_with_key_builder(self):
        redis = AsyncMock()
        key_builder = AsyncMock()
        isolation = RedisEventIsolation(redis=redis, key_builder=key_builder)
        assert isolation.redis is redis
        assert isolation.key_builder is key_builder

    def test_create_from_url(self):
        with patch("redis.asyncio.connection.ConnectionPool.from_url") as pool:
            isolation = RedisEventIsolation.from_url("redis://localhost:6379/0")
            assert isinstance(isolation, RedisEventIsolation)
            assert isolation.redis is not None
            assert isolation.key_builder is not None

            pool.assert_called_once_with("redis://localhost:6379/0")

    @pytest.mark.asyncio
    async def test_close(self):
        isolation = RedisEventIsolation(redis=AsyncMock())
        await isolation.close()

        # close is not called because connection should be closed from the storage
        # assert isolation.redis.close.called_once()
