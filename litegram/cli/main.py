from __future__ import annotations

import importlib
import sys
from typing import TYPE_CHECKING, Any

try:
    import rich_click as click
except ImportError:
    import click  # type: ignore[no-redef]

if TYPE_CHECKING:
    from litegram.dispatcher.dispatcher import Dispatcher


def import_string(import_name: str) -> Any:
    if ":" in import_name:
        module_name, obj_name = import_name.split(":", 1)
    else:
        module_name, obj_name = import_name, None

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Could not import module {module_name!r}") from e

    if obj_name:
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(f"Module {module_name!r} has no attribute {obj_name!r}") from e

    return module


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def litegram_group() -> None:
    """Litegram CLI."""


@litegram_group.group()
def run() -> None:
    """Run bot."""


@run.command(name="polling")
@click.argument("path")
@click.option("--token", help="Bot token", envvar="BOT_TOKEN")
@click.option("--log-level", help="Log level", default="INFO", show_default=True)
def run_polling(path: str, token: str | None, log_level: str) -> None:
    """Run bot in polling mode.

    PATH is a module path to a Dispatcher instance or a factory.
    Example: 'my_bot:dp' or 'my_bot:create_dispatcher'
    """
    import asyncio
    import logging

    from litegram import Bot, Dispatcher

    logging.basicConfig(level=log_level.upper())

    try:
        obj = import_string(path)
    except ImportError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)

    if isinstance(obj, Dispatcher):
        dp = obj
    elif callable(obj):
        dp = obj()
    else:
        dp = obj

    if not isinstance(dp, Dispatcher):
        click.secho(f"Error: {path} must be a Dispatcher instance or a factory returning one.", fg="red", err=True)
        sys.exit(1)

    if not token:
        click.secho("Error: Bot token is required. Use --token or BOT_TOKEN env var.", fg="red", err=True)
        sys.exit(1)

    bot = Bot(token=token)

    click.echo(f"Starting polling for bot {path}...")
    try:
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        click.echo("Stopped.")


@run.command(name="webhook")
@click.argument("path")
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
@click.option("--log-level", help="Log level", default="info", show_default=True)
def run_webhook(path: str, host: str, port: int, log_level: str) -> None:
    """Run bot in webhook mode using Litestar.

    PATH is a module path to a Litestar instance or a factory.
    Example: 'my_bot:app'
    """
    import uvicorn
    from litestar import Litestar

    try:
        obj = import_string(path)
    except ImportError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)

    if isinstance(obj, Litestar):
        app = obj
    elif callable(obj):
        app = obj()
    else:
        app = obj

    if not isinstance(app, Litestar):
        click.secho(f"Error: {path} must be a Litestar instance or a factory returning one.", fg="red", err=True)
        sys.exit(1)

    uvicorn.run(app, host=host, port=port, log_level=log_level.lower())


@litegram_group.command(name="version")
def version_command() -> None:
    """Show litegram version."""
    from litegram import __version__

    click.echo(f"litegram {__version__}")
