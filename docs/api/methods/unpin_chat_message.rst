################
unpinChatMessage
################

Returns: :obj:`bool`

.. automodule:: litegram.methods.unpin_chat_message
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.unpin_chat_message(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.unpin_chat_message import UnpinChatMessage`
- alias: :code:`from litegram.methods import UnpinChatMessage`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(UnpinChatMessage(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return UnpinChatMessage(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.unpin_message`
- :meth:`litegram.types.message.Message.unpin`
