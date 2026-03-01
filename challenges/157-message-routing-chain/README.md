# Challenge 157: Message Routing Chain

## Difficulty: Medium
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

Three agents form a message routing chain: Source, Processor, and Sink. A message must flow through each agent in sequence, being transformed along the way. This tests whether agents can implement a reliable message-passing pipeline.

## Objective

- **Source** creates and sends a message to the Processor
- **Processor** transforms the message payload (uppercase) and forwards to the Sink
- **Sink** receives the final message and extracts the result

## Setup

- `setup/messages/` -- directory for message files (empty at start)

## Steps

1. **Step 1 (Source):** Read `steps/step_1.md`. Create the initial message.
2. **Step 2 (Processor):** Read `steps/step_2.md`. Transform and forward the message.
3. **Step 3 (Sink):** Read `steps/step_3.md`. Extract the final payload.

## Verification

```bash
python tests/verify.py
```

Checks that the message chain is complete: msg_001.json and msg_002.json exist, payload was transformed to uppercase, and answer.txt contains the final payload.
