#########
sendVenue
#########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_venue
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_venue(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_venue import SendVenue`
- alias: :code:`from litegram.methods import SendVenue`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendVenue(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendVenue(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_venue`
- :meth:`litegram.types.message.Message.reply_venue`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_venue`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_venue_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_venue`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_venue`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_venue`
