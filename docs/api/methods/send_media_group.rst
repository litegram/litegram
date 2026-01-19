##############
sendMediaGroup
##############

Returns: :obj:`list[Message]`

.. automodule:: litegram.methods.send_media_group
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: list[Message] = await bot.send_media_group(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_media_group import SendMediaGroup`
- alias: :code:`from litegram.methods import SendMediaGroup`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: list[Message] = await bot(SendMediaGroup(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendMediaGroup(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_media_group`
- :meth:`litegram.types.message.Message.reply_media_group`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_media_group`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_media_group_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_media_group`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_media_group`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_media_group`
