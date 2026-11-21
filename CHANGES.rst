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

1.2.1 (2026-11-21)
===================

Features
--------

- Added official Python 3.15 support (``requires-python = ">=3.13,<3.16"`` and the corresponding classifier).
- Upgraded ``hiredis`` to 3.5.0 and ``watchfiles`` to 1.2.0, whose wheels provide CPython 3.15 binaries; the complete dependency set, including test and documentation extras, now installs on 3.15.

Misc
----

- Cleaned up small test-lint issues, including an explicit timeout in the FSM isolation test and explicit file encodings in ``scripts/bump_version.py``.


1.2.0 (2026-11-21)
===================
===================

Features
--------

- Complete Russian localization of the API types reference: all 430 catalogs (~4730 entries) translated, including the pre-10.4 backlog. Untranslated entries now fall back only for sections outside api/types.

Removals
--------

- Removed the legacy ``.butcher/`` infrastructure: enum configs moved to ``scripts/api_tool/config/enums/``, the schema baseline lives in ``.api/schema.json``, and the fresh parse lands in ``.api/new/``. ``make update-api`` follows the new layout.
- Removed ``litegram.utils.mypy_hacks`` — use ``functools.lru_cache`` directly.

Bugfixes
--------

- Removed ``lru_cache`` from ``Update.event_type``: the cache retained every processed ``Update`` object forever, causing unbounded memory growth under load.

Misc
----

- Generated-file provenance comments rebranded to the litegram api tool; README badge, ``bump_versions.py`` and ``Makefile`` follow the new schema paths.


1.1.0 (2026-11-20)
===================

Features
--------

- Added full support for Telegram Bot API 10.4 (released on November 9, 2026), covering all changes from 9.4 through 10.4:
  rich messages (RichMessage/RichText/RichBlock families), widgets (Widget/WidgetQuery/SharedWidgetQuery),
  ephemeral messages, managed bots, chat join request queries, poll voting enhancements,
  TON wallet cards and the rest of the new types and methods.
- ``HttpxSession`` now accepts ``max_connections`` and ``max_keepalive_connections`` for connection-pool tuning in high-load production.
- File uploads stream through a Litegram-owned async multipart encoder: bounded memory and guaranteed source cleanup instead of the incompatible ``files=`` path.
- Mini App init-data validators accept ``auth_date_timeout`` to reject stale init data (replay protection).
- Polling shutdown drains in-flight update handlers (``drain_timeout``, default 30 s) before closing sessions and FSM storage.

Bugfixes
--------

- Fixed ``Update.purchased_paid_media`` field name (was ``paid_media_purchased``), so the field now correctly deserializes real Telegram payloads and the dispatcher routes the update.
- Fixed deprecated field handling (``Default``/``Field(alias=...)``) across the API layer and preserved curated defaults (e.g. ``RefundedPayment.currency``).
- Restore bounded defaults for the HTTPX connection pool while allowing explicit overrides.
- Route all six new update types through the dispatcher and populate their event context where available.
- Decode ``answerGuestQuery`` as ``SentGuestMessage`` and managed-bot token responses as strings.
- Fix async callable dispatch, class-based error reporting, chat-scoped FSM resolution, nested state names, and keyboard markup option round-trips.
- Reject malformed encoded deep links and third-party Mini App signatures without propagating decoding errors.
- Isolate per-handler context: data injected by a skipped handler's filters no longer leaks into subsequent handlers or outer middlewares.
- Escape URLs in HTML attributes and Markdown link destinations; validate ``pre_language`` tags.
- Use constant-time comparison in Login Widget signature validation.
- ``create_channel_bot_link`` generates ``?startchannel`` links; ``startapp`` payloads follow the 512-character limit.
- ``ChatActionSender`` propagates ``business_connection_id`` and collects background worker failures.

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
