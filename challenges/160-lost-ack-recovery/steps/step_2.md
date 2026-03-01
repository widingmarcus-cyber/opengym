You are the Receiver agent. Your task is to process messages and send acknowledgements — but simulate a network failure where one acknowledgement gets "lost".

1. Read `setup/outbox.json` to see the messages sent by the Sender.
2. Process all messages (you receive all of them successfully).
3. Write acknowledgements to `setup/inbox.json` as a JSON array. Each entry should have `"id"` (matching the message ID) and `"acked": true`.
4. However, you must simulate a **lost acknowledgement**: pick the **second** message in the list and do NOT include its acknowledgement in `inbox.json`.

The Sender will later compare outbox and inbox to detect which message was not acknowledged.
