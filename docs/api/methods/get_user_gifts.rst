############
getUserGifts
############

Returns: :obj:`OwnedGifts`

.. automodule:: litegram.methods.get_user_gifts
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: OwnedGifts = await bot.get_user_gifts(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_user_gifts import GetUserGifts`
- alias: :code:`from litegram.methods import GetUserGifts`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: OwnedGifts = await bot(GetUserGifts(...))
