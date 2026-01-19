#################
promoteChatMember
#################

Returns: :obj:`bool`

.. automodule:: litegram.methods.promote_chat_member
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.promote_chat_member(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.promote_chat_member import PromoteChatMember`
- alias: :code:`from litegram.methods import PromoteChatMember`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(PromoteChatMember(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return PromoteChatMember(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.promote`
