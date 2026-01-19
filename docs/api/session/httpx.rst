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
================================

In order to use HttpxSession with proxy connector you have to install `httpx-socks <https://pypi.org/project/httpx-socks>`_

Binding session to bot:

.. code-block::

    from litegram import Bot
    from litegram.client.session.httpx import HttpxSession

    session = HttpxSession(proxy="protocol://host:port/")
    bot = Bot(token="bot token", session=session)


.. note::

    Only following protocols are supported: http(tunneling), socks4(a), socks5
    as httpx_socks `documentation <https://github.com/romis2012/httpx-socks/blob/master/README.md>`_ claims.


Authorization
-------------

Proxy authorization credentials can be specified in proxy URL or come as an instance of :obj:`httpx.BasicAuth` containing
login and password.

Consider examples:

.. code-block::

    from httpx import BasicAuth
    from litegram.client.session.httpx import HttpxSession

    auth = BasicAuth(login="user", password="password")
    session = HttpxSession(proxy=("protocol://host:port", auth))


or simply include your basic auth credential in URL

.. code-block::

    session = HttpxSession(proxy="protocol://user:password@host:port")


.. note::

    Litegram prefers `BasicAuth` over username and password in URL, so
    if proxy URL contains login and password and `BasicAuth` object is passed at the same time
    litegram will use login and password from `BasicAuth` instance.


Proxy chains
------------

Since `httpx-socks <https://pypi.org/project/httpx-socks/>`_ supports proxy chains, you're able to use them in litegram

Example of chain proxies:

.. code-block::

    from httpx import BasicAuth
    from litegram.client.session.httpx import HttpxSession

    auth = BasicAuth(login="user", password="password")
    session = HttpxSession(
        proxy={
            "protocol0://host0:port0",
            "protocol1://user:password@host1:port1",
            ("protocol2://host2:port2", auth),
        }  # can be any iterable if not set
    )
