You are Node B in a distributed commit protocol. Your task is to cast your vote.

1. Read `setup/votes.json` (contains Node A's vote).
2. Add your vote (`"commit"` with `"timestamp": 2`) under the key `"node_b"` while preserving Node A's entry.

IMPORTANT: You must preserve Node A's vote. Node C is unavailable and will not vote.
