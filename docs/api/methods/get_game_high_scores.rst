#################
getGameHighScores
#################

Returns: :obj:`list[GameHighScore]`

.. automodule:: litegram.methods.get_game_high_scores
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: list[GameHighScore] = await bot.get_game_high_scores(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.get_game_high_scores import GetGameHighScores`
- alias: :code:`from litegram.methods import GetGameHighScores`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: list[GameHighScore] = await bot(GetGameHighScores(...))
