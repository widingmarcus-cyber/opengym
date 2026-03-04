"""Developer command to encrypt test files in challenges."""

import shutil
from pathlib import Path

import click

from cli.crypto import encrypt_bytes
from cli.keys import get_test_encryption_key
from cli.utils import get_challenges_dir, resolve_challenge_ids


@click.command()
@click.argument("challenge_id", default="all")
@click.option("--dry-run", is_flag=True, help="Show what would be encrypted without changing files")
@click.option("--force", is_flag=True, help="Re-encrypt already encrypted files")
def encrypt_tests(challenge_id: str, dry_run: bool, force: bool):
    """Encrypt test files in challenge directories.

    Developer tool. Run after creating or modifying tests.
    Encrypts .py files in tests/ dirs, replacing them with .py.enc files.
    """
    challenges_dir = get_challenges_dir()
    key = get_test_encryption_key()

    if challenge_id == "all":
        dirs = sorted(
            d for d in challenges_dir.iterdir()
            if d.is_dir() and (d / "tests").exists()
        )
    else:
        ids = resolve_challenge_ids(challenge_id, challenges_dir)
        dirs = [challenges_dir / cid for cid in ids if (challenges_dir / cid / "tests").exists()]

    encrypted_count = 0
    skipped_count = 0

    for challenge_dir in dirs:
        tests_dir = challenge_dir / "tests"
        for py_file in sorted(tests_dir.glob("*.py")):
            enc_file = py_file.with_suffix(py_file.suffix + ".enc")

            if enc_file.exists() and not force:
                skipped_count += 1
                continue

            if dry_run:
                click.echo(f"  Would encrypt: {py_file.relative_to(challenges_dir)}")
                encrypted_count += 1
                continue

            plaintext = py_file.read_bytes()
            ciphertext = encrypt_bytes(plaintext, key)
            enc_file.write_bytes(ciphertext)
            py_file.unlink()

            click.echo(f"  Encrypted: {py_file.relative_to(challenges_dir)}")
            encrypted_count += 1

        # Clean __pycache__
        if not dry_run:
            pycache = tests_dir / "__pycache__"
            if pycache.exists():
                shutil.rmtree(pycache)

    action = "Would encrypt" if dry_run else "Encrypted"
    click.echo(f"\n{action}: {encrypted_count} files")
    if skipped_count:
        click.echo(f"Skipped (already encrypted): {skipped_count}")
