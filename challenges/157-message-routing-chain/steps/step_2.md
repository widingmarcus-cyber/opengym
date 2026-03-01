You are the Processor agent. Your task is to read an incoming message, transform its payload, and forward it.

1. Read `setup/messages/msg_001.json`.
2. Transform the `payload` value to UPPERCASE.
3. Write a new message to `setup/messages/msg_002.json`:

```json
{
  "from": "processor",
  "to": "sink",
  "payload": "HELLO WORLD",
  "timestamp": 2
}
```

The `payload` must be the uppercase version of what was in msg_001.json. Keep the routing chain intact: `from` is "processor", `to` is "sink".
