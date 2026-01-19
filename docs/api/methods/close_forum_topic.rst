###############
closeForumTopic
###############

Returns: :obj:`bool`

.. automodule:: litegram.methods.close_forum_topic
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.close_forum_topic(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.close_forum_topic import CloseForumTopic`
- alias: :code:`from litegram.methods import CloseForumTopic`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(CloseForumTopic(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return CloseForumTopic(...)
