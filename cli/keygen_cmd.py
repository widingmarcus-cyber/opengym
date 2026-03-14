"""Generate a local encryption key for private OpenGym test fixtures."""

from pathlib import Path

import click

from cli.keys import create_local_test_key, get_default_key_path


@click.command(name="init-key")
@click.option(
    "--path",
    default=None,
    help="Where to write the key file (default: ~/.opengym/test_key).",
)
@click.option("--force", is_flag=True, help="Overwrite existing key file.")
def init_key(path: str | None, force: bool):
    """Create a local key for encrypting/decrypting private challenge tests."""
    target = Path(path).expanduser().resolve() if path else get_default_key_path()
    try:
        key_path = create_local_test_key(path=target, force=force)
    except FileExistsError as exc:
        click.echo(f"Error: {exc}", err=True)
        click.echo("Use --force to overwrite.", err=True)
        raise SystemExit(1)

    click.echo(f"Created key file: {key_path}")
    click.echo("Set OPENGYM_TEST_KEY_FILE to share this key across machines if needed.")
