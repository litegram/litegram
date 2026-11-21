"""API tooling for litegram.

Parses the Telegram Bot API documentation page into a versioned schema
and generates/enumerates the framework-facing API layer from it.

Layout:
    - ``parse``        — HTML page -> ``.api/schema.json`` (+ per-object entity caches)
    - ``extract_config`` — bootstrap curated configs from existing code
    - ``gen``          — render new files (types/methods/enums/unions)
    - ``patch``        — delta-patch existing files (preserve custom code)
    - ``exports``      — regenerate package ``__init__`` exports
    - ``apply``        — main driver: apply a schema update
    - ``sync_router``  — sync dispatcher observers with Update fields
    - ``docs``         — generate Sphinx docs pages
"""
