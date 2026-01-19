################
getMyStarBalance
################

Returns: :obj:`StarAmount`

.. automodule:: litegram.methods.get_my_star_balance
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: StarAmount = await bot.get_my_star_balance(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_my_star_balance import GetMyStarBalance`
- alias: :code:`from litegram.methods import GetMyStarBalance`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: StarAmount = await bot(GetMyStarBalance(...))
