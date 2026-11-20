=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://pip.pypa.io/en/latest/development/#adding-a-news-entry
    we named the news folder "CHANGES".

    WARNING: Don't drop the next directive!

.. .. towncrier-draft-entries:: [UPCOMING UPDATE]

.. towncrier release notes start

1.1.0 (2026-11-20)
===================

Features
--------

- Added full support for Telegram Bot API 10.4 (released on November 9, 2026), covering all changes from 9.4 through 10.4:
  rich messages (RichMessage/RichText/RichBlock families), widgets (Widget/WidgetQuery/SharedWidgetQuery),
  ephemeral messages, managed bots, chat join request queries, poll voting enhancements,
  TON wallet cards and the rest of the new types and methods.
  `#176.api <https://github.com/litegram/litegram/issues/176.api>`_
- ``HttpxSession`` now accepts ``max_connections`` and ``max_keepalive_connections`` for connection-pool tuning in high-load production.

Bugfixes
--------

- Fixed ``Update.purchased_paid_media`` field name (was ``paid_media_purchased``), so the field now correctly deserializes real Telegram payloads and the dispatcher routes the update.
- Fixed deprecated field handling (``Default``/``Field(alias=...)``) across the API layer and preserved curated defaults (e.g. ``RefundedPayment.currency``).
- Fixed ``HttpxSession.create_client`` race condition: concurrent first requests now share one httpx client.

Improved Documentation
----------------------

- Added API reference pages for all new types and methods, regenerated enums/unions docs.

Misc
----

- Added behavioral tests for the new Bot API 10.4 surface (rich text unions, widget queries, purchased paid media regression, new bot methods) and an UpdateType/Update consistency test.


1.0.10 (2026-01-22)
===================

No significant changes.


1.0.9 (2026-01-21)
===================

No significant changes.


1.0.8 (2026-01-21)
===================

No significant changes.


1.0.7 (2026-01-21)
===================

No significant changes.


1.0.5 (2026-01-21)
===================

No significant changes.


1.0.4 (2026-01-21)
===================

No significant changes.


1.0.0 (2026-01-20)
====================

Features
--------

- Added full support for Telegram Bot API 9.3

Bugfixes
--------

Misc
----
