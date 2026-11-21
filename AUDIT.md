# Litegram 1.1.0 release audit

This review covers the 10.4 API delta and the handwritten dispatcher, webhook, session, filters, handlers, FSM, CLI and utilities. It is a source review with targeted offline regression tests, not a certification or a live Telegram integration test.

## Fixed and tested

- Route all six new update types from raw JSON through the dispatcher and supply their user/chat context when available.
- Decode `answerGuestQuery` as `SentGuestMessage`, and managed-bot token responses as strings. The guest-query regression checks a JSON response at the HTTP boundary.
- Await async callable instances, expose the underlying exception in class-based error handlers, and allow non-scene handlers to run with a scene registry and FSM disabled.
- Resolve chat-scoped FSM keys without a user ID, and refresh deeply nested state names without changing the parent hierarchy.
- Preserve keyboard options when copying or rebuilding markup; explicit options override the saved ones.
- Reject malformed encoded start links and malformed third-party Mini App signatures without propagating a decoding error. Keep HTTPX pool defaults bounded when callers do not override them.
- Stream uploads through a Litegram-owned async multipart encoder (`litegram/client/session/multipart.py`): bounded memory, source generators closed on success, write errors and cancellation; verified against a parsed multipart body, plus lazy-read and cleanup tests.
- Drain in-flight update handlers on polling shutdown before sessions and FSM storage close (`drain_timeout`, default 30 s; stuck handlers are cancelled after the timeout).
- Token-based webhook now requires the acceptable token set up front and rejects unknown URL tokens with 404; `accept_any_token=True` opts back into legacy behavior explicitly.
- Regeneration baseline is canonical: `.butcher/schema.json` mirrors `.api/schema.json`, `apply` promotes the applied schema to the baseline and refuses a no-op run when baseline equals target.

All 31 new methods have offline wrapper coverage. This does not prove that every optional argument combination, result variant or wire payload is correct.

## Release gates still open

| Priority | Finding | Next step |
|---|---|---|
| High | The multipart path sends chunked bodies without `Content-Length`; a deployed Telegram endpoint or proxy may reject chunked uploads, and a nested `URLInputFile` download shares the POST's connection pool. | Verify against the real API (or a local Bot API server) and document/provide a separate source session; add a disk-backed staging mode if `Content-Length` proves mandatory. |
| Medium | Review of utilities surfaced outstanding concerns: callback-data `None` round-trips, markup URL/attribute escaping, Mini App freshness policy, and inconsistent channel/Mini App deep-link helpers. | Address separately with compatibility tests and migration notes. |
| Medium | The review also surfaced remaining task, context and FSM concerns: skipped-handler filter data can leak to later handlers; scene history updates are not transactions; background chat-action errors may not be collected. | Define expected semantics before changing them and exercise the selected production backends. |

## Docs and performance

The English reference and Russian migration guide are supplemented by Russian translations for all 31 new method pages. The type reference and existing catalog are not fully translated.

Run `uv run python -B -m scripts.benchmark_runtime` from the repository root. A local CPython 3.13.15 / Pydantic 2.14.4 run measured **25.22 µs/update** (**39,658 updates/s**). This is the median of five repeated means for sequential `feed_raw_update` from a decoded dictionary, with one async handler and FSM/event logging disabled. It excludes HTTP, JSON parsing, Redis/Mongo, logging, concurrency and application work. Measure p95/p99 latency, memory, queue growth and shutdown under representative traffic before sizing a deployment.
