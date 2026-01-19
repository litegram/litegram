############################
transferBusinessAccountStars
############################

Returns: :obj:`bool`

.. automodule:: litegram.methods.transfer_business_account_stars
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.transfer_business_account_stars(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.transfer_business_account_stars import TransferBusinessAccountStars`
- alias: :code:`from litegram.methods import TransferBusinessAccountStars`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(TransferBusinessAccountStars(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return TransferBusinessAccountStars(...)
