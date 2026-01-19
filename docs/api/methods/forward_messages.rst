###############
forwardMessages
###############

Returns: :obj:`list[MessageId]`

.. automodule:: litegram.methods.forward_messages
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: list[MessageId] = await bot.forward_messages(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.forward_messages import ForwardMessages`
- alias: :code:`from litegram.methods import ForwardMessages`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: list[MessageId] = await bot(ForwardMessages(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return ForwardMessages(...)
