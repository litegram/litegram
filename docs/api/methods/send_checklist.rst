#############
sendChecklist
#############

Returns: :obj:`Message`

.. automodule:: litegram.methods.send_checklist
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: Message = await bot.send_checklist(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.send_checklist import SendChecklist`
- alias: :code:`from litegram.methods import SendChecklist`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: Message = await bot(SendChecklist(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SendChecklist(...)
