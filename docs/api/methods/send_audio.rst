#########
sendAudio
#########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_audio
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_audio(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_audio import SendAudio`
- alias: :code:`from litegram.methods import SendAudio`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendAudio(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendAudio(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_audio`
- :meth:`litegram.types.message.Message.reply_audio`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_audio`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_audio_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_audio`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_audio`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_audio`
