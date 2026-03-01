import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from auth import TokenManager, HARDCODED_TOKEN


def test_rotation_changes_token():
    """rotate_token() must return a NEW token different from the original."""
    mgr = TokenManager()
    old_token = mgr.get_current_token()
    new_token = mgr.rotate_token()
    if new_token == old_token:
        print(json.dumps({"test": "rotation_changes_token", "passed": False,
                          "message": f"rotate_token() returned the same token: '{new_token}'"}))
        return
    if mgr.get_current_token() != new_token:
        print(json.dumps({"test": "rotation_changes_token", "passed": False,
                          "message": "get_current_token() does not return the new token after rotation"}))
        return
    print(json.dumps({"test": "rotation_changes_token", "passed": True, "message": "OK"}))


def test_new_token_authenticates():
    """The new token after rotation must authenticate successfully."""
    mgr = TokenManager()
    new_token = mgr.rotate_token()
    result = mgr.authenticate(new_token)
    if result.get("status") != "ok":
        print(json.dumps({"test": "new_token_authenticates", "passed": False,
                          "message": f"New token failed to authenticate: {result}"}))
        return
    print(json.dumps({"test": "new_token_authenticates", "passed": True, "message": "OK"}))


def test_previous_token_grace_period():
    """The previous token should still work during the grace period (one rotation)."""
    mgr = TokenManager()
    first_token = mgr.get_current_token()
    mgr.rotate_token()
    # Previous token should still authenticate
    result = mgr.authenticate(first_token)
    if result.get("status") != "ok":
        print(json.dumps({"test": "previous_token_grace_period", "passed": False,
                          "message": f"Previous token rejected during grace period: {result}"}))
        return
    print(json.dumps({"test": "previous_token_grace_period", "passed": True, "message": "OK"}))


def test_old_old_token_rejected():
    """A token from two rotations ago must be rejected."""
    mgr = TokenManager()
    original_token = mgr.get_current_token()
    mgr.rotate_token()  # rotation 1
    mgr.rotate_token()  # rotation 2 — original should now be rejected
    result = mgr.authenticate(original_token)
    if result.get("status") != "denied":
        print(json.dumps({"test": "old_old_token_rejected", "passed": False,
                          "message": f"Token from 2 rotations ago was still accepted: {result}"}))
        return
    print(json.dumps({"test": "old_old_token_rejected", "passed": True, "message": "OK"}))


def test_tokens_are_cryptographic():
    """Rotated tokens must be generated with the secrets module (not hardcoded)."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "auth.py")
    with open(source_path, "r") as f:
        source = f.read()
    if "secrets" not in source:
        print(json.dumps({"test": "tokens_are_cryptographic", "passed": False,
                          "message": "auth.py does not use the 'secrets' module for token generation"}))
        return
    # Verify that two rotations produce different tokens
    mgr = TokenManager()
    t1 = mgr.rotate_token()
    t2 = mgr.rotate_token()
    if t1 == t2:
        print(json.dumps({"test": "tokens_are_cryptographic", "passed": False,
                          "message": f"Two consecutive rotations produced the same token: '{t1}'"}))
        return
    if len(t1) < 32:
        print(json.dumps({"test": "tokens_are_cryptographic", "passed": False,
                          "message": f"Token too short ({len(t1)} chars) — should be at least 32"}))
        return
    print(json.dumps({"test": "tokens_are_cryptographic", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_rotation_changes_token()
    test_new_token_authenticates()
    test_previous_token_grace_period()
    test_old_old_token_rejected()
    test_tokens_are_cryptographic()
