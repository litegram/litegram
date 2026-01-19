######################
removeChatVerification
######################

Returns: :obj:`bool`

.. automodule:: litegram.methods.remove_chat_verification
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.remove_chat_verification(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.remove_chat_verification import RemoveChatVerification`
- alias: :code:`from litegram.methods import RemoveChatVerification`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(RemoveChatVerification(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return RemoveChatVerification(...)
