Use Custom API server
=====================

For example, if you want to use self-hosted API server:

.. code-block:: python

    session = HttpxSession(
        api=TelegramAPIServer.from_base('http://localhost:8082')
    )
    bot = Bot(..., session=session)

.. autoclass:: litegram.client.telegram.TelegramAPIServer
    :members:
