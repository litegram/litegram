##################
setChatPermissions
##################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_chat_permissions
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_chat_permissions(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_chat_permissions import SetChatPermissions`
- alias: :code:`from litegram.methods import SetChatPermissions`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetChatPermissions(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetChatPermissions(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.set_permissions`
