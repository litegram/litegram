.. _webhook:

#######
Webhook
#######

Telegram Bot API supports webhook.
If you set webhook for your bot, Telegram will send updates to the specified url.
You can use :meth:`litegram.methods.set_webhook.SetWebhook` method to specify a url
and receive incoming updates on it.

.. note::

    If you use webhook, you can't use long polling at the same time.

Before start i'll recommend you to read `official Telegram's documentation about webhook <https://core.telegram.org/bots/webhooks>`_

After you read it, you can start to read this section.

Generally to use webhook with litegram you should use any async web framework.
By out of the box litegram has an httpx integration, so we'll use it.

.. note::

    You can use any async web framework you want, but you should write your own integration if you don't use httpx.


httpx integration
===================

Out of the box litegram has httpx integration, so you can use it.

Here is available few ways to do it using different implementations of the webhook controller:

- :class:`litegram.webhook.litestar_server.BaseRequestHandler` - Abstract class for httpx webhook controller
- :class:`litegram.webhook.litestar_server.SimpleRequestHandler`  - Simple webhook controller, uses single Bot instance
- :class:`litegram.webhook.litestar_server.TokenBasedRequestHandler`  - Token based webhook controller, uses multiple Bot instances and tokens

You can use it as is or inherit from it and override some methods.

.. autoclass:: litegram.webhook.litestar_server.BaseRequestHandler
    :members: __init__, register, close, resolve_bot, verify_secret, handle

.. autoclass:: litegram.webhook.litestar_server.SimpleRequestHandler
    :members: __init__, register, close, resolve_bot, verify_secret, handle

.. autoclass:: litegram.webhook.litestar_server.TokenBasedRequestHandler
    :members: __init__, register, close, resolve_bot, verify_secret, handle

Security
--------

Telegram supports two methods to verify incoming requests that they are from Telegram:

Using a secret token
~~~~~~~~~~~~~~~~~~~~

When you set webhook, you can specify a secret token and then use it to verify incoming requests.

Using IP filtering
~~~~~~~~~~~~~~~~~~

You can specify a list of IP addresses from which you expect incoming requests, and then use it to verify incoming requests.

It can be acy using firewall rules or nginx configuration or middleware on application level.

So, litegram has an implementation of the IP filtering middleware for httpx.

.. autofunction:: litegram.webhook.litestar_server.ip_filter_middleware

.. autoclass:: litegram.webhook.security.IPFilter
    :members: __init__, allow, allow_ip, default, check

Examples
--------

Behind reverse proxy
~~~~~~~~~~~~~~~~~~~~

In this example we'll use httpx as web framework and nginx as reverse proxy.

.. literalinclude:: ../../examples/echo_bot_webhook.py

When you use nginx as reverse proxy, you should set `proxy_pass` to your httpx server address.

.. code-block:: nginx

    location /webhook {
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass http://127.0.0.1:8080;
    }


Without reverse proxy (not recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case without using reverse proxy, you can use httpx's ssl context.

Also this example contains usage with self-signed certificate.

.. literalinclude:: ../../examples/echo_bot_webhook_ssl.py


With using other web framework
==============================

You can pass incoming request to litegram's webhook controller from any web framework you want.

Read more about it in :meth:`litegram.dispatcher.dispatcher.Dispatcher.feed_webhook_update`
or :meth:`litegram.dispatcher.dispatcher.Dispatcher.feed_update` methods.

.. code-block:: python

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)


.. note::

    If you want to use reply into webhook, you should check that result of the :code:`feed_update`
    methods is an instance of API method and build :code:`multipart/form-data`
    or :code:`application/json` response body manually.
