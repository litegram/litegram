####################
deleteStickerFromSet
####################

Returns: :obj:`bool`

.. automodule:: litegram.methods.delete_sticker_from_set
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: bool = await bot.delete_sticker_from_set(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.delete_sticker_from_set import DeleteStickerFromSet`
- alias: :code:`from litegram.methods import DeleteStickerFromSet`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: bool = await bot(DeleteStickerFromSet(...))

As reply into Webhook in handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    return DeleteStickerFromSet(...)


As shortcut from received object
--------------------------------

- :meth:`litegram.types.sticker.Sticker.delete_from_set`
