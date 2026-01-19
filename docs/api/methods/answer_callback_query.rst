###################
answerCallbackQuery
###################

Returns: :obj:`bool`

.. automodule:: litegram.methods.answer_callback_query
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.answer_callback_query(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.answer_callback_query import AnswerCallbackQuery`
- alias: :code:`from litegram.methods import AnswerCallbackQuery`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(AnswerCallbackQuery(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return AnswerCallbackQuery(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.callback_query.CallbackQuery.answer`
