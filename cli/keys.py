"""Key material for test file encryption.

Stored in CLI code (not in challenges/) so agents cannot access it.
This is obfuscation against automated agents, not defense against
determined human attackers.
"""

import hashlib

_PASSPHRASE = b"opengym-test-protection-v1-do-not-share-with-agents"


def get_test_encryption_key() -> bytes:
    return hashlib.sha256(_PASSPHRASE).digest()
