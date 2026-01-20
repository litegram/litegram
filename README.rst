########
litegram
########

.. image:: https://img.shields.io/pypi/l/litegram?style=flat-square
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/pypi/status/litegram?style=flat-square
    :target: https://pypi.python.org/pypi/litegram
    :alt: PyPi status

.. image:: https://img.shields.io/pypi/v/litegram?style=flat-square
    :target: https://pypi.python.org/pypi/litegram
    :alt: PyPi Package Version

.. image:: https://img.shields.io/pypi/dm/litegram?style=flat-square
    :target: https://pypi.python.org/pypi/litegram
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/litegram?style=flat-square
    :target: https://pypi.python.org/pypi/litegram
    :alt: Supported python versions

.. image:: https://img.shields.io/badge/dynamic/json?color=blue&logo=telegram&label=Telegram%20Bot%20API&query=%24.api.version&url=https%3A%2F%2Fraw.githubusercontent.com%2Flitegram%2Flitegram%2Fmaster%2F.butcher%2Fschema%2Fschema.json&style=flat-square
    :target: https://core.telegram.org/bots/api
    :alt: Telegram Bot API

.. image:: https://img.shields.io/github/actions/workflow/status/litegram/litegram/tests.yml?branch=master&style=flat-square
    :target: https://github.com/litegram/litegram/actions
    :alt: Tests

.. image:: https://img.shields.io/codecov/c/github/litegram/litegram?style=flat-square
    :target: https://app.codecov.io/gh/litegram/litegram
    :alt: Codecov

**litegram** is a modern and fully asynchronous framework for
`Telegram Bot API <https://core.telegram.org/bots/api>`_ written in Python 3.13+ using
`litestar <https://github.com/litestar-org/litestar>`_ and
`httpx <https://github.com/encode/httpx>`_.

Make your bots faster and more powerful!

Documentation:
 - 🇷🇺 `Russian <https://docs.litegram.dev/ru/master/>`_
 - 🇺🇸 `English <https://docs.litegram.dev/en/master/>`_


Features
========

- Asynchronous (`asyncio docs <https://docs.python.org/3/library/asyncio.html>`_, :pep:`492`)
- Has type hints (:pep:`484`) and can be used with `ty <https://github.com/v999/ty>`_
- Supports `Telegram Bot API 9.3 <https://core.telegram.org/bots/api>`_ and gets fast updates to the latest versions of the Bot API
- Updates router (Blueprints)
- Has Finite State Machine
- Uses powerful `magic filters <https://docs.litegram.dev/en/latest/dispatcher/filters/magic_filters.html#magic-filters>`_
- Middlewares (incoming updates and API calls)
- Provides `Replies into Webhook <https://core.telegram.org/bots/faq#how-can-i-make-requests-in-response-to-updates>`_
- Integrated I18n/L10n support with GNU Gettext (or Fluent)


.. warning::

    It is strongly advised that you have prior experience working
    with `asyncio <https://docs.python.org/3/library/asyncio.html>`_
    before beginning to use **litegram**.

    If you have any questions, you can visit our community chats on Telegram:

    - 🇷🇺 `@litegram_ru <https://t.me/litegram_ru>`_
    - 🇺🇸 `@litegram_en <https://t.me/litegram_en>`_
