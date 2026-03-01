You are the Sender agent. Your task is to send 3 messages by writing them to an outbox.

Write the following to `setup/outbox.json`:

```json
[
  {"id": "m1", "content": "hello", "acked": false},
  {"id": "m2", "content": "world", "acked": false},
  {"id": "m3", "content": "test", "acked": false}
]
```

All messages start with `"acked": false`. The Receiver will acknowledge them in the next step.
