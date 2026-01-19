##############
getWebhookInfo
##############

Returns: :obj:`WebhookInfo`

.. automodule:: litegram.methods.get_webhook_info
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: WebhookInfo = await bot.get_webhook_info(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_webhook_info import GetWebhookInfo`
- alias: :code:`from litegram.methods import GetWebhookInfo`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: WebhookInfo = await bot(GetWebhookInfo(...))
