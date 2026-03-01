# Challenge 160: Lost Acknowledgement Recovery

## Difficulty: Hard
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

A sender-receiver system where acknowledgements can be "lost". The sender must detect unacknowledged messages and identify which ones need to be resent. This tests reliable delivery patterns in multi-agent communication.

## Objective

- **Sender** sends 3 messages via an outbox
- **Receiver** processes all messages but "loses" one acknowledgement
- **Sender** detects the missing ack and identifies the unacknowledged message

## Setup

- `setup/` -- empty directory at start

## Steps

1. **Step 1 (Sender):** Read `steps/step_1.md`. Write 3 messages to the outbox.
2. **Step 2 (Receiver):** Read `steps/step_2.md`. Acknowledge messages but "lose" one ack.
3. **Step 3 (Sender check):** Read `steps/step_3.md`. Detect unacknowledged messages.

## Verification

```bash
python tests/verify.py
```

Checks that answer.json correctly identifies the unacked message, outbox.json has correct ack states, and inbox.json exists.
