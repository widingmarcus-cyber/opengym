"""Key management for test file encryption."""

import hashlib
import os
import secrets
from pathlib import Path

_LEGACY_PASSPHRASE = b"opengym-test-protection-v1-do-not-share-with-agents"
_DEFAULT_KEY_PATH = Path.home() / ".opengym" / "test_key"


def _derive_key(material: bytes) -> bytes:
    return hashlib.sha256(material).digest()


def get_default_key_path() -> Path:
    return _DEFAULT_KEY_PATH


def _load_primary_key_material() -> bytes | None:
    """Load preferred key material from env or key file."""
    env_key = os.environ.get("OPENGYM_TEST_KEY")
    if env_key:
        return env_key.encode("utf-8")

    key_file = Path(os.environ.get("OPENGYM_TEST_KEY_FILE", str(_DEFAULT_KEY_PATH)))
    if key_file.exists():
        try:
            data = key_file.read_bytes().strip()
            if data:
                return data
        except OSError:
            return None
    return None


def get_test_encryption_key() -> bytes:
    """Return the primary key used for encrypting new test fixtures."""
    material = _load_primary_key_material()
    if material:
        return _derive_key(material)
    return _derive_key(_LEGACY_PASSPHRASE)


def get_test_decryption_keys() -> list[bytes]:
    """Return candidate keys used when decrypting fixtures.

    Includes the primary key and the legacy fallback key for backwards
    compatibility with existing public challenge files.
    """
    keys: list[bytes] = []
    primary = get_test_encryption_key()
    keys.append(primary)

    legacy = _derive_key(_LEGACY_PASSPHRASE)
    if legacy != primary:
        keys.append(legacy)
    return keys


def create_local_test_key(path: Path | None = None, force: bool = False) -> Path:
    """Create a local per-install key file for hardened private suites."""
    target = path or get_default_key_path()
    if target.exists() and not force:
        raise FileExistsError(f"Key file already exists: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    secret = secrets.token_urlsafe(48)
    target.write_text(secret + "\n", encoding="utf-8")
    return target
