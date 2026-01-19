###########
sendMessage
###########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_message
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_message(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_message import SendMessage`
- alias: :code:`from litegram.methods import SendMessage`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendMessage(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendMessage(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer`
- :meth:`litegram.types.message.Message.reply`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply`
