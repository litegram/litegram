################
sendMessageDraft
################

Returns: :obj:`bool`

.. automodule:: litegram.methods.send_message_draft
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.send_message_draft(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_message_draft import SendMessageDraft`
- alias: :code:`from litegram.methods import SendMessageDraft`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SendMessageDraft(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendMessageDraft(...)
