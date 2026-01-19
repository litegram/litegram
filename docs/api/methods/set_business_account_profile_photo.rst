##############################
setBusinessAccountProfilePhoto
##############################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_business_account_profile_photo
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_business_account_profile_photo(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_business_account_profile_photo import SetBusinessAccountProfilePhoto`
- alias: :code:`from litegram.methods import SetBusinessAccountProfilePhoto`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetBusinessAccountProfilePhoto(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetBusinessAccountProfilePhoto(...)
