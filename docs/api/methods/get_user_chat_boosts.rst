#################
getUserChatBoosts
#################

Returns: :obj:`UserChatBoosts`

.. automodule:: litegram.methods.get_user_chat_boosts
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: UserChatBoosts = await bot.get_user_chat_boosts(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_user_chat_boosts import GetUserChatBoosts`
- alias: :code:`from litegram.methods import GetUserChatBoosts`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: UserChatBoosts = await bot(GetUserChatBoosts(...))
