#################
answerWebAppQuery
#################

Returns: :obj:`SentWebAppMessage`

.. automodule:: litegram.methods.answer_web_app_query
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: SentWebAppMessage = await bot.answer_web_app_query(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.answer_web_app_query import AnswerWebAppQuery`
- alias: :code:`from litegram.methods import AnswerWebAppQuery`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: SentWebAppMessage = await bot(AnswerWebAppQuery(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return AnswerWebAppQuery(...)
