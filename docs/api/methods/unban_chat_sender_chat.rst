###################
unbanChatSenderChat
###################

Returns: :obj:`bool`

.. automodule:: litegram.methods.unban_chat_sender_chat
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.unban_chat_sender_chat(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.unban_chat_sender_chat import UnbanChatSenderChat`
- alias: :code:`from litegram.methods import UnbanChatSenderChat`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(UnbanChatSenderChat(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return UnbanChatSenderChat(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.unban_sender_chat`
