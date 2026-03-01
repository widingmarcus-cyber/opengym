You are the Receiver agent. Your task is to process messages and send acknowledgements -- but one ack gets "lost".

1. Read `setup/outbox.json` to see the 3 messages sent by the Sender.
2. Process all messages (you receive all 3).
3. Write acknowledgements to `setup/inbox.json`, but simulate a "lost" acknowledgement for message m2:

```json
[
  {"id": "m1", "acked": true},
  {"id": "m3", "acked": true}
]
```

Note: Only m1 and m3 are acknowledged. The acknowledgement for m2 is "lost" (not included in inbox.json).
