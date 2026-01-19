###########
sendInvoice
###########

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_invoice
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_invoice(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_invoice import SendInvoice`
- alias: :code:`from litegram.methods import SendInvoice`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendInvoice(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendInvoice(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.message.Message.answer_invoice`
- :meth:`litegram.types.message.Message.reply_invoice`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_invoice`
- :meth:`litegram.types.chat_join_request.ChatJoinRequest.answer_invoice_pm`
- :meth:`litegram.types.chat_member_updated.ChatMemberUpdated.answer_invoice`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.answer_invoice`
- :meth:`litegram.types.inaccessible_message.InaccessibleMessage.reply_invoice`
