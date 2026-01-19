#######################
giftPremiumSubscription
#######################

Returns: :obj:`bool`

.. automodule:: litegram.methods.gift_premium_subscription
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.gift_premium_subscription(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.gift_premium_subscription import GiftPremiumSubscription`
- alias: :code:`from litegram.methods import GiftPremiumSubscription`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(GiftPremiumSubscription(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return GiftPremiumSubscription(...)
