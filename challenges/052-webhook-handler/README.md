# Challenge 052: Webhook Handler

## Difficulty: Medium

## Task

Build a webhook receiver with HMAC signature validation and event routing. Implement the `WebhookHandler` class in `setup/webhook.py`.

## Requirements

### `WebhookHandler` class

1. `register(event_type, callback)` — Register a callback function for a specific event type. The callback receives the parsed event data dict and returns a result.
2. `verify_signature(payload_bytes, signature, secret)` — Verify the HMAC-SHA256 signature of the payload. `payload_bytes` is bytes, `signature` is a hex string, and `secret` is a string. Returns `True` if valid, `False` otherwise.
3. `handle(raw_payload, signature, secret)` — Process an incoming webhook:
   - Verify the signature (raise `ValueError` with message `"Invalid signature"` if invalid)
   - Parse the JSON payload (must contain `"event"` and `"data"` keys)
   - Route to the registered callback for the event type (raise `ValueError` with message `"Unknown event: <event_type>"` if no callback is registered)
   - Return the callback's result

## Rules

- Only modify files in the `setup/` directory
- Use `hmac` and `hashlib` from the standard library
- The HMAC digest should use SHA-256 and compare using `hmac.compare_digest`
