# Litegram 1.1.0 release audit

This review covers the 10.4 API delta and the handwritten dispatcher, webhook, session, filters, handlers, FSM, CLI and utilities. It is a source review with targeted offline regression tests, not a certification or a live Telegram integration test.

## Security scan status

A Mimosa deep scan (`scan-2026-11-21T06-05-22.736Z-77d00af05764`, seal `sha256:5b60dd…bb32c`) over the current tree reports **0 findings** (dependency scan: 109 packages, 0 affected). The tool marks its own coverage as *partial / inconclusive*, so this is not a security certification — the flagged pre-commit findings (test temp file, examples with hardcoded secrets, docs-fetch SSRF surface) were fixed and the full static path analysis did not complete on this codebase size.

## Fixed and tested

- Route all six new update types from raw JSON through the dispatcher and supply their user/chat context when available.
- Decode `answerGuestQuery` as `SentGuestMessage`, and managed-bot token responses as strings. The guest-query regression checks a JSON response at the HTTP boundary.
- Await async callable instances, expose the underlying exception in class-based error handlers, and allow non-scene handlers to run with a scene registry and FSM disabled.
- Resolve chat-scoped FSM keys without a user ID, and refresh deeply nested state names without changing the parent hierarchy.
- Preserve keyboard options when copying or rebuilding markup; explicit options override the saved ones.
- Reject malformed encoded start links and malformed third-party Mini App signatures without propagating a decoding error. Keep HTTPX pool defaults bounded when callers do not override them.
- Escape URLs in HTML attributes and Markdown destinations (`hlink`/`hide_link`/`link`), validate `pre_language` tags, use constant-time comparison in Login Widget validation, generate `?startchannel` links from `create_channel_bot_link`, apply the 512-char payload limit to `startapp` links, and propagate `business_connection_id` through `ChatActionSender` and its middleware.
- Document callback-data `None` round-trip semantics (positional format: an explicit `None` on a field with a default unpacks as the default).
- Mini App init-data validators accept an optional `auth_date_timeout` (seconds): stale data is rejected with `ValueError`, replaying captured init data no longer passes indefinitely.
- Handler attempts run on isolated context copies in `TelegramEventObserver.trigger`: data injected by a skipped handler's filters no longer leaks into later handlers or outer middlewares (regression-tested).
- The `ChatActionSender` worker logs its own failures and its final result is retrieved on stop, so background Telegram errors no longer linger as unobserved task exceptions.
- Stream uploads through a Litegram-owned async multipart encoder (`litegram/client/session/multipart.py`): bounded memory, source generators closed on success, write errors and cancellation; verified against a parsed multipart body, plus lazy-read and cleanup tests.
- Drain in-flight update handlers on polling shutdown before sessions and FSM storage close (`drain_timeout`, default 30 s; stuck handlers are cancelled after the timeout).
- Token-based webhook now requires the acceptable token set up front and rejects unknown URL tokens with 404; `accept_any_token=True` opts back into legacy behavior explicitly.
- Regeneration baseline is canonical: `.butcher/schema.json` mirrors `.api/schema.json`, `apply` promotes the applied schema to the baseline and refuses a no-op run when baseline equals target.

All 31 new methods have offline wrapper coverage. This does not prove that every optional argument combination, result variant or wire payload is correct.

## Release gates still open

| Priority | Finding | Next step |
|---|---|---|
| High | The multipart path sends chunked bodies without `Content-Length`. A real-socket e2e now proves our wire format (chunked framing, multipart structure, closing delimiter) is correct end-to-end, but whether a deployed Telegram endpoint or proxy accepts chunked uploads still needs one live call; a nested `URLInputFile` download also shares the POST's connection pool. | One live-API verification with a real bot token; document/provide a separate source session; add a disk-backed staging mode if `Content-Length` proves mandatory. |
| Medium | Scene history updates are not storage transactions; concurrent processing outside the isolation scope can lose history entries. | Decide on transactional semantics and exercise the selected production backends. |

## Docs and performance

The English reference and Russian migration guide are supplemented by Russian translations for all 31 new method pages. The type reference and existing catalog are not fully translated.

Run `uv run python -B -m scripts.benchmark_runtime` from the repository root. A local CPython 3.13.15 / Pydantic 2.14.4 run measured **25.22 µs/update** (**39,658 updates/s**). This is the median of five repeated means for sequential `feed_raw_update` from a decoded dictionary, with one async handler and FSM/event logging disabled. It excludes HTTP, JSON parsing, Redis/Mongo, logging, concurrency and application work. Measure p95/p99 latency, memory, queue growth and shutdown under representative traffic before sizing a deployment.
