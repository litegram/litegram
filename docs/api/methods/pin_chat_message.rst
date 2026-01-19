##############
pinChatMessage
##############

Returns: :obj:`bool`

.. automodule:: litegram.methods.pin_chat_message
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.pin_chat_message(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.pin_chat_message import PinChatMessage`
- alias: :code:`from litegram.methods import PinChatMessage`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(PinChatMessage(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return PinChatMessage(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.pin_message`
- :meth:`litegram.types.message.Message.pin`
