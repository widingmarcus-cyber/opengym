"""Encrypt/decrypt test files to prevent agents from reading answers.

Uses HMAC-SHA256 as a stream cipher with PBKDF2 key derivation.
Stdlib-only — no external dependencies.
"""

import base64
import hashlib
import hmac
import os
import struct
from pathlib import Path

HEADER = b"OPENGYM-ENC-V1"
SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 32
KDF_ITERATIONS = 10_000


def _derive_key(password: bytes, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password, salt, KDF_ITERATIONS)


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    stream = bytearray()
    counter = 0
    while len(stream) < length:
        block = hmac.new(
            key, nonce + struct.pack("<Q", counter), hashlib.sha256
        ).digest()
        stream.extend(block)
        counter += 1
    return bytes(stream[:length])


def _xor(data: bytes, ks: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, ks))


def encrypt_bytes(plaintext: bytes, password: bytes) -> bytes:
    """Encrypt plaintext, return header + base64 blob."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = _derive_key(password, salt)
    ciphertext = _xor(plaintext, _keystream(key, nonce, len(plaintext)))
    tag = hmac.new(key, salt + nonce + ciphertext, hashlib.sha256).digest()
    blob = salt + nonce + ciphertext + tag
    return HEADER + b"\n" + base64.b64encode(blob)


def decrypt_bytes(data: bytes, password: bytes) -> bytes:
    """Decrypt a blob produced by encrypt_bytes."""
    if not data.startswith(HEADER):
        raise ValueError("Not an OpenGym encrypted file")
    b64_part = data[len(HEADER):].strip()
    blob = base64.b64decode(b64_part)
    salt = blob[:SALT_SIZE]
    nonce = blob[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
    tag = blob[-TAG_SIZE:]
    ciphertext = blob[SALT_SIZE + NONCE_SIZE : -TAG_SIZE]
    key = _derive_key(password, salt)
    expected_tag = hmac.new(key, salt + nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected_tag):
        raise ValueError("Integrity check failed: file tampered or wrong key")
    return _xor(ciphertext, _keystream(key, nonce, len(ciphertext)))


def encrypt_file(src: Path, dest: Path, password: bytes):
    dest.write_bytes(encrypt_bytes(src.read_bytes(), password))


def decrypt_file(src: Path, dest: Path, password: bytes):
    dest.write_bytes(decrypt_bytes(src.read_bytes(), password))
