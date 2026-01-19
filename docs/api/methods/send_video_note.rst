#############
sendVideoNote
#############

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_video_note
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_video_note(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_video_note import SendVideoNote`
- alias: :code:`from litegram.methods import SendVideoNote`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendVideoNote(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendVideoNote(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_video_note`
- :meth:`litegram.types.message.Message.reply_video_note`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_video_note`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_video_note_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_video_note`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_video_note`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_video_note`
