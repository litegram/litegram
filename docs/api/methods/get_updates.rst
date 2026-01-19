##########
getUpdates
##########

Returns: :obj:`list[Update]`

.. automodule:: litegram.methods.get_updates
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: list[Update] = await bot.get_updates(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_updates import GetUpdates`
- alias: :code:`from litegram.methods import GetUpdates`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: list[Update] = await bot(GetUpdates(...))
