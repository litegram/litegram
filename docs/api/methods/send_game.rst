########
sendGame
########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_game
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_game(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_game import SendGame`
- alias: :code:`from litegram.methods import SendGame`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendGame(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendGame(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_game`
- :meth:`litegram.types.message.Message.reply_game`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_game`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_game_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_game`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_game`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_game`
