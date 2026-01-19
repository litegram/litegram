############
getChatGifts
############

Returns: :obj:`OwnedGifts`

.. automodule:: litegram.methods.get_chat_gifts
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: OwnedGifts = await bot.get_chat_gifts(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_chat_gifts import GetChatGifts`
- alias: :code:`from litegram.methods import GetChatGifts`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: OwnedGifts = await bot(GetChatGifts(...))
