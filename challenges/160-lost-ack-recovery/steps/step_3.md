You are the Sender agent again. Your task is to detect which messages were not acknowledged and handle recovery.

1. Read `setup/inbox.json` (acknowledgements from the Receiver).
2. Read `setup/outbox.json` (your original messages).
3. Compare: find messages in outbox that are NOT acknowledged in inbox.
4. Update `setup/outbox.json`: mark m1 and m3 as `"acked": true`. Leave m2 as `"acked": false`.
5. Write `setup/answer.json` with:

```json
{
  "unacked": ["m2"],
  "total_sent": 3,
  "total_acked": 2
}
```

The `unacked` array lists the IDs of messages that were not acknowledged. `total_sent` is the total number of messages sent. `total_acked` is the number of messages that received acknowledgements.
