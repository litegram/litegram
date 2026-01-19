################
setMyDescription
################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_my_description
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_my_description(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_my_description import SetMyDescription`
- alias: :code:`from litegram.methods import SetMyDescription`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetMyDescription(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetMyDescription(...)
