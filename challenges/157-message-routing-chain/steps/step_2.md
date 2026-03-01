You are the Processor agent. Your task is to read an incoming message, transform its payload, and forward it.

1. Read `setup/messages/msg_001.json`.
2. Transform the `payload` value to UPPERCASE.
3. Write a new message to `setup/messages/msg_002.json` with:
   - `"from"`: `"processor"`
   - `"to"`: `"sink"`
   - `"payload"`: the uppercase version of the payload from msg_001.json
   - `"timestamp"`: `2`

Keep the routing chain intact.
