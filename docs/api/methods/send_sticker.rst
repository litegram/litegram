###########
sendSticker
###########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_sticker
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_sticker(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_sticker import SendSticker`
- alias: :code:`from litegram.methods import SendSticker`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendSticker(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendSticker(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_sticker`
- :meth:`litegram.types.message.Message.reply_sticker`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_sticker`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_sticker_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_sticker`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_sticker`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_sticker`
