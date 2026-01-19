##################
getChatMemberCount
##################

Returns: :obj:`int`

.. automodule:: litegram.methods.get_chat_member_count
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: int = await bot.get_chat_member_count(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_chat_member_count import GetChatMemberCount`
- alias: :code:`from litegram.methods import GetChatMemberCount`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: int = await bot(GetChatMemberCount(...))




As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.get_member_count`
