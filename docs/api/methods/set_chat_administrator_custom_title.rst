###############################
setChatAdministratorCustomTitle
###############################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_chat_administrator_custom_title
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_chat_administrator_custom_title(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_chat_administrator_custom_title import SetChatAdministratorCustomTitle`
- alias: :code:`from litegram.methods import SetChatAdministratorCustomTitle`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetChatAdministratorCustomTitle(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetChatAdministratorCustomTitle(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.chat.Chat.set_administrator_custom_title`
