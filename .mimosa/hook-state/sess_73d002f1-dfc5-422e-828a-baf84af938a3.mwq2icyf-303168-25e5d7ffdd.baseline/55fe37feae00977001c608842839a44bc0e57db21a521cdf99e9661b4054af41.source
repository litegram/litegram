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


@litegram_group.group()
def bot() -> None:
    """Bot management."""


@bot.command(name="info")
@click.option("--token", help="Bot token", envvar="BOT_TOKEN")
def bot_info(token: str | None) -> None:
    """Get bot information."""
    import asyncio

    from litegram import Bot
    from litegram.exceptions import TelegramAPIError

    if not token:
        click.secho("Error: Bot token is required. Use --token or BOT_TOKEN env var.", fg="red", err=True)
        sys.exit(1)

    async def get_info() -> None:
        async with Bot(token=token) as bot:
            try:
                user = await bot.get_me()
                click.secho("Bot information:", fg="green", bold=True)
                click.echo(f"  ID:       {user.id}")
                click.echo(f"  Name:     {user.first_name}")
                click.echo(f"  Username: @{user.username}")
                click.echo(f"  Can join groups:   {user.can_join_groups}")
                click.echo(f"  Can read messages: {user.can_read_all_group_messages}")
                click.echo(f"  Supports inline:   {user.supports_inline_queries}")
            except TelegramAPIError as e:
                click.secho(f"Error: {e}", fg="red", err=True)
                sys.exit(1)

    asyncio.run(get_info())


@litegram_group.group()
def i18n() -> None:
    """Manage bot translations."""


@i18n.command(name="extract")
@click.option("-d", "--domain", default="messages", show_default=True)
@click.option("-p", "--path", default="locales", show_default=True)
@click.option("-i", "--input", "input_path", default=".", show_default=True)
def i18n_extract(domain: str, path: str, input_path: str) -> None:
    """Extract messages from source code."""
    from babel.messages.frontend import CommandLineInterface

    click.echo(f"Extracting messages to {path}/{domain}.pot...")
    CommandLineInterface().run(
        [
            "pybabel",
            "extract",
            input_path,
            "-o",
            f"{path}/{domain}.pot",
            "--project",
            "litegram-bot",
        ]
    )


@i18n.command(name="init")
@click.option("-d", "--domain", default="messages", show_default=True)
@click.option("-p", "--path", default="locales", show_default=True)
@click.argument("locale")
def i18n_init(domain: str, path: str, locale: str) -> None:
    """Initialize a new locale."""
    from babel.messages.frontend import CommandLineInterface

    click.echo(f"Initializing locale {locale}...")
    CommandLineInterface().run(
        [
            "pybabel",
            "init",
            "-i",
            f"{path}/{domain}.pot",
            "-d",
            path,
            "-D",
            domain,
            "-l",
            locale,
        ]
    )


@i18n.command(name="update")
@click.option("-d", "--domain", default="messages", show_default=True)
@click.option("-p", "--path", default="locales", show_default=True)
def i18n_update(domain: str, path: str) -> None:
    """Update existing locales from POT file."""
    from babel.messages.frontend import CommandLineInterface

    click.echo(f"Updating locales in {path}...")
    CommandLineInterface().run(
        [
            "pybabel",
            "update",
            "-i",
            f"{path}/{domain}.pot",
            "-d",
            path,
            "-D",
            domain,
        ]
    )


@i18n.command(name="compile")
@click.option("-d", "--domain", default="messages", show_default=True)
@click.option("-p", "--path", default="locales", show_default=True)
def i18n_compile(domain: str, path: str) -> None:
    """Compile locales."""
    from babel.messages.frontend import CommandLineInterface

    click.echo(f"Compiling locales in {path}...")
    CommandLineInterface().run(
        [
            "pybabel",
            "compile",
            "-d",
            path,
            "-D",
            domain,
        ]
    )


@litegram_group.command(name="version")
def version_command() -> None:
    """Show litegram version."""
    from litegram import __version__

    click.echo(f"litegram {__version__}")
