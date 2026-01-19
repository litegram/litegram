#################
createInvoiceLink
#################

Returns: :obj:`str`

.. automodule:: litegram.methods.create_invoice_link
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: str = await bot.create_invoice_link(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.create_invoice_link import CreateInvoiceLink`
- alias: :code:`from litegram.methods import CreateInvoiceLink`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: str = await bot(CreateInvoiceLink(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return CreateInvoiceLink(...)
