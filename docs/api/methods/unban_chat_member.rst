###############
unbanChatMember
###############

Returns: :obj:`bool`

.. automodule:: litegram.methods.unban_chat_member
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.unban_chat_member(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.unban_chat_member import UnbanChatMember`
- alias: :code:`from litegram.methods import UnbanChatMember`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(UnbanChatMember(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return UnbanChatMember(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.unban`
