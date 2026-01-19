###################
answerShippingQuery
###################

Returns: :obj:`bool`

.. automodule:: litegram.methods.answer_shipping_query
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.answer_shipping_query(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.answer_shipping_query import AnswerShippingQuery`
- alias: :code:`from litegram.methods import AnswerShippingQuery`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(AnswerShippingQuery(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return AnswerShippingQuery(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.shipping_query.ShippingQuery.answer`
