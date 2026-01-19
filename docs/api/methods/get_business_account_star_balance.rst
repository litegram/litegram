#############################
getBusinessAccountStarBalance
#############################

Returns: :obj:`StarAmount`

.. automodule:: litegram.methods.get_business_account_star_balance
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: StarAmount = await bot.get_business_account_star_balance(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_business_account_star_balance import GetBusinessAccountStarBalance`
- alias: :code:`from litegram.methods import GetBusinessAccountStarBalance`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: StarAmount = await bot(GetBusinessAccountStarBalance(...))
