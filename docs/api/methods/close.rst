#####
close
#####

Returns: :obj:`bool`

.. automodule:: litegram.methods.close
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.close(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.close import Close`
- alias: :code:`from litegram.methods import Close`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(Close(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return Close(...)
