from __future__ import annotations

import pytest
from pymongo.errors import PyMongoError

from litegram.fsm.state import State
from litegram.fsm.storage.mongo import MongoStorage
from litegram.fsm.storage.pymongo import PyMongoStorage
from tests.conftest import CHAT_ID, USER_ID

PREFIX = "fsm"


@pytest.fixture()
def any_mongo_storage(request):
    return request.getfixturevalue(request.param)


def pytest_generate_tests(metafunc):
    if "any_mongo_storage" in metafunc.fixturenames:
        metafunc.parametrize("any_mongo_storage", ["mongo_storage", "pymongo_storage"], indirect=True)


@pytest.mark.asyncio
async def test_get_storage_passing_only_url(mongo_server):
    # Test MongoStorage
    storage = MongoStorage.from_url(url=mongo_server)
    try:
        await storage._client.server_info()
    except PyMongoError as e:
        pytest.fail(str(e))
    finally:
        await storage.close()

    # Test PyMongoStorage
    storage = PyMongoStorage.from_url(url=mongo_server)
    try:
        await storage._client.server_info()
    except PyMongoError as e:
        pytest.fail(str(e))
    finally:
        await storage.close()


@pytest.mark.asyncio
async def test_storage_close_does_not_throw(mongo_server):
    for storage_class in [MongoStorage, PyMongoStorage]:
        storage = storage_class.from_url(url=mongo_server)
        try:
            await storage.close()
        except Exception as e:
            pytest.fail(f"{storage_class.__name__}.close() raised an exception: {e}")


@pytest.mark.asyncio
async def test_update_not_existing_data_with_empty_dictionary(
    any_mongo_storage: MongoStorage | PyMongoStorage,
    storage_key,
):
    assert await any_mongo_storage._collection.find_one({}) is None
    assert await any_mongo_storage.get_data(key=storage_key) == {}
    assert await any_mongo_storage.update_data(key=storage_key, data={}) == {}
    assert await any_mongo_storage._collection.find_one({}) is None


@pytest.mark.asyncio
async def test_update_not_existing_data_with_non_empty_dictionary(
    any_mongo_storage: MongoStorage | PyMongoStorage,
    storage_key,
):
    assert await any_mongo_storage._collection.find_one({}) is None
    assert await any_mongo_storage.update_data(key=storage_key, data={"key": "value"}) == {"key": "value"}
    assert await any_mongo_storage._collection.find_one({}) == {
        "_id": f"{PREFIX}:{CHAT_ID}:{USER_ID}",
        "data": {"key": "value"},
    }
    await any_mongo_storage._collection.delete_one({})


@pytest.mark.asyncio
async def test_update_existing_data_with_empty_dictionary(
    any_mongo_storage: MongoStorage | PyMongoStorage,
    storage_key,
):
    assert await any_mongo_storage._collection.find_one({}) is None
    await any_mongo_storage.set_data(key=storage_key, data={"key": "value"})
    assert await any_mongo_storage.update_data(key=storage_key, data={}) == {"key": "value"}
    assert await any_mongo_storage._collection.find_one({}) == {
        "_id": f"{PREFIX}:{CHAT_ID}:{USER_ID}",
        "data": {"key": "value"},
    }
    await any_mongo_storage._collection.delete_one({})


@pytest.mark.asyncio
async def test_update_existing_data_with_non_empty_dictionary(
    any_mongo_storage: MongoStorage | PyMongoStorage,
    storage_key,
):
    assert await any_mongo_storage._collection.find_one({}) is None
    await any_mongo_storage.set_data(key=storage_key, data={"key": "value"})
    assert await any_mongo_storage.update_data(key=storage_key, data={"key": "new_value"}) == {"key": "new_value"}
    assert await any_mongo_storage._collection.find_one({}) == {
        "_id": f"{PREFIX}:{CHAT_ID}:{USER_ID}",
        "data": {"key": "new_value"},
    }
    await any_mongo_storage._collection.delete_one({})


@pytest.mark.asyncio
async def test_document_life_cycle(
    any_mongo_storage: MongoStorage | PyMongoStorage,
    storage_key,
):
    assert await any_mongo_storage._collection.find_one({}) is None
    await any_mongo_storage.set_state(storage_key, "test")
    await any_mongo_storage.set_data(storage_key, {"key": "value"})
    assert await any_mongo_storage._collection.find_one({}) == {
        "_id": f"{PREFIX}:{CHAT_ID}:{USER_ID}",
        "state": "test",
        "data": {"key": "value"},
    }
    await any_mongo_storage.set_state(storage_key, None)
    assert await any_mongo_storage._collection.find_one({}) == {
        "_id": f"{PREFIX}:{CHAT_ID}:{USER_ID}",
        "data": {"key": "value"},
    }
    await any_mongo_storage.set_data(storage_key, {})
    assert await any_mongo_storage._collection.find_one({}) is None


class TestStateAndDataDoNotAffectEachOther:
    @pytest.mark.asyncio
    async def test_state_and_data_do_not_affect_each_other_while_getting(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        assert await any_mongo_storage._collection.find_one({}) is None
        await any_mongo_storage.set_state(storage_key, "test")
        await any_mongo_storage.set_data(storage_key, {"key": "value"})
        assert await any_mongo_storage.get_state(storage_key) == "test"
        assert await any_mongo_storage.get_data(storage_key) == {"key": "value"}

    @pytest.mark.asyncio
    async def test_data_do_not_affect_to_deleted_state_getting(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        await any_mongo_storage.set_data(storage_key, {"key": "value"})
        await any_mongo_storage.set_state(storage_key, None)
        assert await any_mongo_storage.get_state(storage_key) is None

    @pytest.mark.asyncio
    async def test_state_do_not_affect_to_deleted_data_getting(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        await any_mongo_storage.set_data(storage_key, {"key": "value"})
        await any_mongo_storage.set_data(storage_key, {})
        assert await any_mongo_storage.get_data(storage_key) == {}

    @pytest.mark.asyncio
    async def test_state_do_not_affect_to_updating_not_existing_data_with_empty_dictionary(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {"state": "test"}
        assert await any_mongo_storage.update_data(key=storage_key, data={}) == {}
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {"state": "test"}

    @pytest.mark.asyncio
    async def test_state_do_not_affect_to_updating_not_existing_data_with_non_empty_dictionary(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {"state": "test"}
        assert await any_mongo_storage.update_data(
            key=storage_key,
            data={"key": "value"},
        ) == {"key": "value"}
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {
            "state": "test",
            "data": {"key": "value"},
        }

    @pytest.mark.asyncio
    async def test_state_do_not_affect_to_updating_existing_data_with_empty_dictionary(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        await any_mongo_storage.set_data(storage_key, {"key": "value"})
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {
            "state": "test",
            "data": {"key": "value"},
        }
        assert await any_mongo_storage.update_data(key=storage_key, data={}) == {"key": "value"}
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {
            "state": "test",
            "data": {"key": "value"},
        }

    @pytest.mark.asyncio
    async def test_state_do_not_affect_to_updating_existing_data_with_non_empty_dictionary(
        self,
        any_mongo_storage: MongoStorage | PyMongoStorage,
        storage_key,
    ):
        await any_mongo_storage.set_state(storage_key, "test")
        await any_mongo_storage.set_data(storage_key, {"key": "value"})
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {
            "state": "test",
            "data": {"key": "value"},
        }
        assert await any_mongo_storage.update_data(
            key=storage_key,
            data={"key": "VALUE", "key_2": "value_2"},
        ) == {"key": "VALUE", "key_2": "value_2"}
        assert await any_mongo_storage._collection.find_one({}, projection={"_id": 0}) == {
            "state": "test",
            "data": {"key": "VALUE", "key_2": "value_2"},
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value,result",
    [
        [None, None],
        ["", ""],
        ["text", "text"],
        [State(), None],
        [State(state="*"), "*"],
        [State("text"), "@:text"],
        [State("test", group_name="Test"), "Test:test"],
        [[1, 2, 3], "[1, 2, 3]"],
    ],
)
async def test_resolve_state(value, result, any_mongo_storage: MongoStorage | PyMongoStorage):
    assert any_mongo_storage.resolve_state(value) == result
