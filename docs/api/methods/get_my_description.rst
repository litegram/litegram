################
getMyDescription
################

Returns: :obj:`BotDescription`

.. automodule:: litegram.methods.get_my_description
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: BotDescription = await bot.get_my_description(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_my_description import GetMyDescription`
- alias: :code:`from litegram.methods import GetMyDescription`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: BotDescription = await bot(GetMyDescription(...))
