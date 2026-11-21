#######
httpx
#######

HttpxSession represents a wrapper-class around `ClientSession` from `httpx <https://pypi.org/project/httpx/>`_

Currently `HttpxSession` is a default session used in `litegram.Bot`

.. autoclass:: litegram.client.session.httpx.HttpxSession

Usage example
=============

.. code-block::

    from litegram import Bot
    from litegram.client.session.httpx import HttpxSession

    session = HttpxSession()
    bot = Bot('42:token', session=session)


Proxy requests in HttpxSession
==============================

HTTP and HTTPS proxies work with the base HTTPX installation. For SOCKS5 proxies,
install the optional native HTTPX SOCKS support:

.. code-block:: bash

    pip install "litegram[proxy]"

Bind the session to the bot and pass a proxy URL:

.. code-block::

    from litegram import Bot
    from litegram.client.session.httpx import HttpxSession

    session = HttpxSession(proxy="http://host:port")
    bot = Bot(token="bot token", session=session)

For a SOCKS5 proxy, use a ``socks5`` or ``socks5h`` URL:

.. code-block::

    session = HttpxSession(proxy="socks5://host:port")

.. note::

    HTTPX supports the ``http``, ``https``, ``socks5`` and ``socks5h`` proxy
    schemes. The ``socks5h`` scheme delegates DNS resolution to the proxy.
    SOCKS4 and proxy chains are not supported by this session.


Authorization
-------------

Include the proxy username and password in the URL. Percent-encode special
characters in credentials:

.. code-block::

    session = HttpxSession(proxy="http://user:password@host:port")
    socks_session = HttpxSession(proxy="socks5://user:password@host:port")

``HttpxSession`` passes this URL directly to :class:`httpx.AsyncClient`.
