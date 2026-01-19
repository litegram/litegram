####################
approveSuggestedPost
####################

Returns: :obj:`bool`

.. automodule:: litegram.methods.approve_suggested_post
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.approve_suggested_post(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.approve_suggested_post import ApproveSuggestedPost`
- alias: :code:`from litegram.methods import ApproveSuggestedPost`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(ApproveSuggestedPost(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return ApproveSuggestedPost(...)
