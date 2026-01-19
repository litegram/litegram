####################
deleteChatStickerSet
####################

Returns: :obj:`bool`

.. automodule:: litegram.methods.delete_chat_sticker_set
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.delete_chat_sticker_set(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.delete_chat_sticker_set import DeleteChatStickerSet`
- alias: :code:`from litegram.methods import DeleteChatStickerSet`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(DeleteChatStickerSet(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return DeleteChatStickerSet(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.delete_sticker_set`
