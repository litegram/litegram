#############
sendAnimation
#############

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_animation
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_animation(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_animation import SendAnimation`
- alias: :code:`from litegram.methods import SendAnimation`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendAnimation(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendAnimation(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_animation`
- :meth:`litegram.types.message.Message.reply_animation`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_animation`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_animation_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_animation`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_animation`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_animation`
