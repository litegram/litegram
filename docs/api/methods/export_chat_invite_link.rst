####################
exportChatInviteLink
####################

Returns: :obj:`str`

.. automodule:: litegram.methods.export_chat_invite_link
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: str = await bot.export_chat_invite_link(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.export_chat_invite_link import ExportChatInviteLink`
- alias: :code:`from litegram.methods import ExportChatInviteLink`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: str = await bot(ExportChatInviteLink(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return ExportChatInviteLink(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.export_invite_link`
