#################
uploadStickerFile
#################

Returns: :obj:`File`

.. automodule:: litegram.methods.upload_sticker_file
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields


Usage
=====

As bot method
-------------

.. code-block::

    result: File = await bot.upload_sticker_file(...)


Method as object
----------------

Imports:

- :code:`from litegram.methods.upload_sticker_file import UploadStickerFile`
- alias: :code:`from litegram.methods import UploadStickerFile`

With specific bot
~~~~~~~~~~~~~~~~~

.. code-block:: python

    result: File = await bot(UploadStickerFile(...))
