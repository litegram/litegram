from __future__ import annotations

import asyncio
import sys
import weakref
from pathlib import Path

import pytest
from _pytest.config import UsageError  # noqa: PLC2701 — pytest's documented helper
from pymongo.errors import InvalidURI, PyMongoError
from pymongo.uri_parser import parse_uri as parse_mongo_url
from redis.asyncio.connection import parse_url as parse_redis_url
from redis.exceptions import ConnectionError as RedisConnectionError

from litegram import Dispatcher
from litegram.fsm.storage.base import StorageKey
from litegram.fsm.storage.memory import (
    DisabledEventIsolation,
    MemoryStorage,
    SimpleEventIsolation,
)
from litegram.fsm.storage.mongo import MongoStorage
from litegram.fsm.storage.pymongo import PyMongoStorage
from litegram.fsm.storage.redis import RedisStorage
from tests.mocked_bot import MockedBot

DATA_DIR = Path(__file__).parent / "data"

CHAT_ID = -42
USER_ID = 42

SKIP_MESSAGE_PATTERN = 'Need "--{db}" option with {db} URI to run'
INVALID_URI_PATTERN = "Invalid {db} URI {uri!r}: {err}"

# Track every selector loop created in the test process so orphaned ones
# (left by the anyio pytest plugin) can be closed promptly.
_TRACKED_LOOPS: weakref.WeakSet = weakref.WeakSet()
_SELECTOR_LOOP_INIT = asyncio.selector_events.BaseSelectorEventLoop.__init__


def _track_selector_loop(self, *args, **kwargs) -> None:
    _SELECTOR_LOOP_INIT(self, *args, **kwargs)
    _TRACKED_LOOPS.add(self)


asyncio.selector_events.BaseSelectorEventLoop.__init__ = _track_selector_loop


def pytest_addoption(parser):
    parser.addoption("--redis", default=None, help="run tests which require redis connection")
    parser.addoption("--mongo", default=None, help="run tests which require mongo connection")


@pytest.fixture(autouse=True)
def close_orphan_event_loops():
    """Close event loops abandoned by the test runner after each test.

    The anyio pytest plugin leaves one unclosed selector loop behind per
    session; when the garbage collector collects it inside a test that uses
    ``pytest.warns``, the unrelated ResourceWarning breaks the assertion
    under ``filterwarnings = error``.
    """
    yield
    for loop in list(_TRACKED_LOOPS):
        if not loop.is_closed() and not loop.is_running():
            loop.close()
            _TRACKED_LOOPS.discard(loop)


def pytest_configure(config):
    config.addinivalue_line("markers", "redis: marked tests require redis connection to run")
    config.addinivalue_line("markers", "mongo: marked tests require mongo connection to run")

    if sys.platform == "win32" and sys.version_info < (3, 14):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Compile locales
    try:
        from babel.messages.mofile import write_mo
        from babel.messages.pofile import read_po

        for path in DATA_DIR.rglob("*.po"):
            mo_path = path.with_suffix(".mo")
            with path.open("rb") as f_po:
                catalog = read_po(f_po)
            with mo_path.open("wb") as f_mo:
                write_mo(f_mo, catalog, use_fuzzy=True)
    except ImportError:
        pass


@pytest.fixture()
def redis_server(request):
    redis_uri = request.config.getoption("--redis")
    if redis_uri is None:
        pytest.skip(SKIP_MESSAGE_PATTERN.format(db="redis"))
    else:
        return redis_uri


@pytest.fixture()
async def redis_storage(redis_server):
    try:
        parse_redis_url(redis_server)
    except ValueError as e:
        raise UsageError(INVALID_URI_PATTERN.format(db="redis", uri=redis_server, err=e)) from e
    storage = RedisStorage.from_url(redis_server)
    try:
        await storage.redis.info()
    except RedisConnectionError as e:
        pytest.fail(str(e))
    try:
        yield storage
    finally:
        conn = await storage.redis
        await conn.flushdb()
        await storage.close()


@pytest.fixture()
def mongo_server(request):
    mongo_uri = request.config.getoption("--mongo")
    if mongo_uri is None:
        pytest.skip(SKIP_MESSAGE_PATTERN.format(db="mongo"))
    else:
        return mongo_uri


@pytest.fixture()
async def mongo_storage(mongo_server):
    try:
        parse_mongo_url(mongo_server)
    except InvalidURI as e:
        raise UsageError(INVALID_URI_PATTERN.format(db="mongo", uri=mongo_server, err=e)) from e
    storage = MongoStorage.from_url(
        url=mongo_server,
        connection_kwargs={"serverSelectionTimeoutMS": 2000},
    )
    try:
        await storage._client.server_info()
    except PyMongoError as e:
        pytest.fail(str(e))
    else:
        yield storage
        await storage._client.drop_database(storage._database)
    finally:
        await storage.close()


@pytest.fixture()
def pymongo_server(request):
    mongo_uri = request.config.getoption("--mongo")
    if mongo_uri is None:
        pytest.skip(SKIP_MESSAGE_PATTERN.format(db="mongo"))
    else:
        return mongo_uri


@pytest.fixture()
async def pymongo_storage(pymongo_server):
    try:
        parse_mongo_url(pymongo_server)
    except InvalidURI as e:
        raise UsageError(INVALID_URI_PATTERN.format(db="mongo", uri=pymongo_server, err=e)) from e
    storage = PyMongoStorage.from_url(
        url=pymongo_server,
        connection_kwargs={"serverSelectionTimeoutMS": 2000},
    )
    try:
        await storage._client.server_info()
    except PyMongoError as e:
        pytest.fail(str(e))
    else:
        yield storage
        await storage._client.drop_database(storage._database)
    finally:
        await storage.close()


@pytest.fixture()
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture()
async def redis_isolation(redis_storage):
    return redis_storage.create_isolation()


@pytest.fixture()
async def lock_isolation():
    isolation = SimpleEventIsolation()
    try:
        yield isolation
    finally:
        await isolation.close()


@pytest.fixture()
async def disabled_isolation():
    isolation = DisabledEventIsolation()
    try:
        yield isolation
    finally:
        await isolation.close()


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def bot():
    return MockedBot()


@pytest.fixture(name="storage_key")
def create_storage_key(bot: MockedBot):
    return StorageKey(chat_id=CHAT_ID, user_id=USER_ID, bot_id=bot.id)


@pytest.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture()
def storage(request):
    return request.getfixturevalue(request.param)


@pytest.fixture()
def isolation(request):
    return request.getfixturevalue(request.param)


def pytest_generate_tests(metafunc):
    if "storage" in metafunc.fixturenames:
        params = ["memory_storage"]
        if metafunc.config.getoption("--redis"):
            params.append("redis_storage")
        if metafunc.config.getoption("--mongo"):
            params.extend(["mongo_storage", "pymongo_storage"])
        metafunc.parametrize("storage", params, indirect=True)
    if "isolation" in metafunc.fixturenames:
        params = ["lock_isolation", "disabled_isolation"]
        if metafunc.config.getoption("--redis"):
            params.append("redis_isolation")
        metafunc.parametrize("isolation", params, indirect=True)


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--mongo"):
        items[:] = [item for item in items if "test_mongodb.py" not in str(item.path)]
    if not config.getoption("--redis"):
        items[:] = [item for item in items if "test_redis.py" not in str(item.path)]


# @pytest.fixture(scope="session")
# def event_loop_policy(request):
#     if sys.platform == "win32":
#         return asyncio.WindowsSelectorEventLoopPolicy()
#     return asyncio.DefaultEventLoopPolicy()
