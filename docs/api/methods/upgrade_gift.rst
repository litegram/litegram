###########
upgradeGift
###########

Returns: :obj:`bool`

.. automodule:: litegram.methods.upgrade_gift
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.upgrade_gift(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.upgrade_gift import UpgradeGift`
- alias: :code:`from litegram.methods import UpgradeGift`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(UpgradeGift(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return UpgradeGift(...)
