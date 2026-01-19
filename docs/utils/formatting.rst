.. _formatting-tool:

==========
Formatting
==========

Make your message formatting flexible and simple

This instrument works on top of Message entities instead of using HTML or Markdown markups,
you can easily construct your message and sent it to the Telegram without the need to
remember tag parity (opening and closing) or escaping user input.

Usage
=====

Basic scenario
--------------

Construct your message and send it to the Telegram.

.. code-block:: python

    content = Text("Hello, ", Bold(message.from_user.full_name), "!")
    await message.answer(**content.as_kwargs())

Is the same as the next example, but without usage markup

.. code-block:: python

    await message.answer(
        text=f"Hello, <b>{html.quote(message.from_user.full_name)}</b>!",
        parse_mode=ParseMode.HTML
    )

Literally when you execute :code:`as_kwargs` method the Text object is converted
into text :code:`Hello, Alex!` with entities list :code:`[MessageEntity(type='bold', offset=7, length=4)]`
and passed into dict which can be used as :code:`**kwargs` in API call.

The complete list of elements is listed `on this page below <#available-elements>`_.

Advanced scenario
-----------------

On top of base elements can be implemented content rendering structures,
so, out of the box litegram has a few already implemented functions that helps you to format
your messages:

.. autofunction:: litegram.utils.formatting.as_line

.. autofunction:: litegram.utils.formatting.as_list

.. autofunction:: litegram.utils.formatting.as_marked_list

.. autofunction:: litegram.utils.formatting.as_numbered_list

.. autofunction:: litegram.utils.formatting.as_section

.. autofunction:: litegram.utils.formatting.as_marked_section

.. autofunction:: litegram.utils.formatting.as_numbered_section

.. autofunction:: litegram.utils.formatting.as_key_value

and lets complete them all:

.. code-block:: python

    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )

Will be rendered into:

  **Success:**

  ✅ Test 1

  ✅ Test 3

  ✅ Test 4

  **Failed:**

  ❌ Test 2

  **Summary:**

   **Total**: 4

   **Success**: 3

   **Failed**: 1

  #test


Or as HTML:

.. code-block:: html

    <b>Success:</b>
    ✅ Test 1
    ✅ Test 3
    ✅ Test 4

    <b>Failed:</b>
    ❌ Test 2

    <b>Summary:</b>
      <b>Total:</b> 4
      <b>Success:</b> 3
      <b>Failed:</b> 1

    #test

Available methods
=================

.. autoclass:: litegram.utils.formatting.Text
    :members:
    :show-inheritance:
    :member-order: bysource
    :special-members: __init__


Available elements
==================

.. autoclass:: litegram.utils.formatting.Text
    :show-inheritance:
    :noindex:

.. autoclass:: litegram.utils.formatting.HashTag
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.CashTag
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.BotCommand
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Url
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Email
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.PhoneNumber
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Bold
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Italic
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Underline
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Strikethrough
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Spoiler
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Code
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.Pre
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.TextLink
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.TextMention
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.CustomEmoji
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.BlockQuote
    :show-inheritance:

.. autoclass:: litegram.utils.formatting.ExpandableBlockQuote
    :show-inheritance:
