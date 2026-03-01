"""Fetch challenges from GitHub or local repo."""

import shutil
from pathlib import Path

import click

from cli.utils import get_challenges_dir, get_workspace_dir, resolve_challenge_ids


@click.command()
@click.argument("challenge_id", default="all")
@click.option("--output", "-o", default=None, help="Output directory (default: ./opengym-workspace)")
def fetch(challenge_id: str, output: str | None):
    """Download a challenge to work on.

    CHALLENGE_ID can be a number (001), a name (fix-syntax-error), or 'all'.
    """
    challenges_dir = get_challenges_dir()
    workspace = Path(output) if output else get_workspace_dir()

    ids = resolve_challenge_ids(challenge_id, challenges_dir)
    if not ids:
        click.echo(f"Error: Challenge '{challenge_id}' not found.", err=True)
        raise SystemExit(1)

    for cid in ids:
        src = challenges_dir / cid
        dest = workspace / cid

        if dest.exists():
            click.echo(f"  {cid}: already exists, skipping (use --output to fetch elsewhere)")
            continue

        # Copy the challenge folder to workspace
        shutil.copytree(src, dest)
        click.echo(f"  {cid}: fetched -> {dest}")

    click.echo(f"\nWorkspace: {workspace}")
    click.echo("Your agent should read the README.md in each challenge folder.")
    click.echo("Only modify files inside setup/. Run 'opengym score <id>' when done.")
