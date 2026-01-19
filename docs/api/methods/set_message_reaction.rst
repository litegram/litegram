##################
setMessageReaction
##################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_message_reaction
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_message_reaction(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_message_reaction import SetMessageReaction`
- alias: :code:`from litegram.methods import SetMessageReaction`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetMessageReaction(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetMessageReaction(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.react`
