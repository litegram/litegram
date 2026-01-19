########
Storages
########

Storages out of the box
=======================

MemoryStorage
-------------

.. autoclass:: litegram.fsm.storage.memory.MemoryStorage
    :members: __init__
    :member-order: bysource

RedisStorage
------------

.. autoclass:: litegram.fsm.storage.redis.RedisStorage
    :members: __init__, from_url
    :member-order: bysource

MongoStorage
------------

.. autoclass:: litegram.fsm.storage.pymongo.PyMongoStorage
    :members: __init__, from_url
    :member-order: bysource

.. autoclass:: litegram.fsm.storage.mongo.MongoStorage
    :members: __init__, from_url
    :member-order: bysource

KeyBuilder
------------

Keys inside Redis and Mongo storages can be customized via key builders:

.. autoclass:: litegram.fsm.storage.base.KeyBuilder
    :members:
    :member-order: bysource

.. autoclass:: litegram.fsm.storage.base.DefaultKeyBuilder
    :members:
    :member-order: bysource


Writing own storages
====================

.. autoclass:: litegram.fsm.storage.base.BaseStorage
    :members:
    :member-order: bysource
