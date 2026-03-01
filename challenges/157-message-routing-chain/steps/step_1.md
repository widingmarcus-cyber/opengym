You are the Source agent. Your task is to create the first message in a routing chain.

Write the following message to `setup/messages/msg_001.json`:

```json
{
  "from": "source",
  "to": "processor",
  "payload": "hello world",
  "timestamp": 1
}
```

This message will be picked up by the Processor agent in the next step.
