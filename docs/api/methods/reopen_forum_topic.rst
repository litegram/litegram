################
reopenForumTopic
################

Returns: :obj:`bool`

.. automodule:: litegram.methods.reopen_forum_topic
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.reopen_forum_topic(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.reopen_forum_topic import ReopenForumTopic`
- alias: :code:`from litegram.methods import ReopenForumTopic`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(ReopenForumTopic(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return ReopenForumTopic(...)
