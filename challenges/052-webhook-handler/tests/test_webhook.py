"""Tests for Challenge 052: Webhook Handler."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import hmac
import hashlib
import json
import pytest
from webhook import WebhookHandler


def make_signed_payload(data, secret):
    payload = json.dumps(data).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return payload, sig


def test_verify_valid_signature():
    handler = WebhookHandler()
    payload = b'{"event": "push", "data": {}}'
    secret = "mysecret"
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    assert handler.verify_signature(payload, sig, secret) is True


def test_verify_invalid_signature():
    handler = WebhookHandler()
    payload = b'{"event": "push", "data": {}}'
    assert handler.verify_signature(payload, "invalidsig", "mysecret") is False


def test_handle_valid_event():
    handler = WebhookHandler()
    handler.register("push", lambda data: {"processed": True, "ref": data.get("ref")})
    secret = "secret123"
    payload_data = {"event": "push", "data": {"ref": "main"}}
    payload, sig = make_signed_payload(payload_data, secret)
    result = handler.handle(payload, sig, secret)
    assert result == {"processed": True, "ref": "main"}


def test_handle_invalid_signature_raises():
    handler = WebhookHandler()
    handler.register("push", lambda data: None)
    payload = b'{"event": "push", "data": {}}'
    with pytest.raises(ValueError, match="Invalid signature"):
        handler.handle(payload, "badsig", "mysecret")


def test_handle_unknown_event_raises():
    handler = WebhookHandler()
    handler.register("push", lambda data: None)
    secret = "mysecret"
    payload_data = {"event": "deploy", "data": {}}
    payload, sig = make_signed_payload(payload_data, secret)
    with pytest.raises(ValueError, match="Unknown event: deploy"):
        handler.handle(payload, sig, secret)


def test_register_multiple_events():
    handler = WebhookHandler()
    handler.register("push", lambda data: "pushed")
    handler.register("pull_request", lambda data: "pr_opened")
    secret = "key"

    payload1, sig1 = make_signed_payload({"event": "push", "data": {}}, secret)
    payload2, sig2 = make_signed_payload({"event": "pull_request", "data": {}}, secret)

    assert handler.handle(payload1, sig1, secret) == "pushed"
    assert handler.handle(payload2, sig2, secret) == "pr_opened"


def test_callback_receives_data_only():
    received = {}

    def on_push(data):
        received.update(data)
        return "ok"

    handler = WebhookHandler()
    handler.register("push", on_push)
    secret = "s"
    payload_data = {"event": "push", "data": {"branch": "dev", "commit": "abc123"}}
    payload, sig = make_signed_payload(payload_data, secret)
    handler.handle(payload, sig, secret)
    assert received == {"branch": "dev", "commit": "abc123"}


def test_different_secrets_fail():
    handler = WebhookHandler()
    handler.register("push", lambda data: "ok")
    payload_data = {"event": "push", "data": {}}
    payload, sig = make_signed_payload(payload_data, "secret_a")
    with pytest.raises(ValueError, match="Invalid signature"):
        handler.handle(payload, sig, "secret_b")
