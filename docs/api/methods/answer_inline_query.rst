#################
answerInlineQuery
#################

Returns: :obj:`bool`

.. automodule:: litegram.methods.answer_inline_query
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.answer_inline_query(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.answer_inline_query import AnswerInlineQuery`
- alias: :code:`from litegram.methods import AnswerInlineQuery`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(AnswerInlineQuery(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return AnswerInlineQuery(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.inline_query.InlineQuery.answer`
