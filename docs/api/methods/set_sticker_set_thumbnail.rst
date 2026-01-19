######################
setStickerSetThumbnail
######################

Returns: :obj:`bool`

.. automodule:: litegram.methods.set_sticker_set_thumbnail
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.set_sticker_set_thumbnail(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.set_sticker_set_thumbnail import SetStickerSetThumbnail`
- alias: :code:`from litegram.methods import SetStickerSetThumbnail`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(SetStickerSetThumbnail(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return SetStickerSetThumbnail(...)
