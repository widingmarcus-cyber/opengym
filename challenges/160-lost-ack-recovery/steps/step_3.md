You are the Sender agent again. Your task is to detect which messages were not acknowledged and handle recovery.

1. Read `setup/inbox.json` (acknowledgements from the Receiver).
2. Read `setup/outbox.json` (your original messages).
3. Compare: find messages in outbox that are NOT acknowledged in inbox.
4. Update `setup/outbox.json`: mark acknowledged messages as `"acked": true`. Leave unacknowledged messages as `"acked": false`.
5. Write `setup/answer.json` with:
   - `"unacked"`: array of message IDs that were not acknowledged
   - `"total_sent"`: total number of messages in outbox
   - `"total_acked"`: number of messages that received acknowledgements
