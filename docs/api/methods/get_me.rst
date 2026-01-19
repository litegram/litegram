#####
getMe
#####

Returns: :obj:`User`

.. automodule:: litegram.methods.get_me
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: User = await bot.get_me(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_me import GetMe`
- alias: :code:`from litegram.methods import GetMe`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: User = await bot(GetMe(...))
