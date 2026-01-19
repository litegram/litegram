##################
restrictChatMember
##################

Returns: :obj:`bool`

.. automodule:: litegram.methods.restrict_chat_member
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.restrict_chat_member(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.restrict_chat_member import RestrictChatMember`
- alias: :code:`from litegram.methods import RestrictChatMember`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(RestrictChatMember(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return RestrictChatMember(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.restrict`
