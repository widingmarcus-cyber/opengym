# Challenge 240: Consensus Simulation

## Objective

Simulate a consensus protocol among distributed nodes. Given a set of nodes with initial proposals and a network topology (which nodes can communicate), simulate rounds of voting until consensus is reached or a maximum number of rounds is exhausted.

## Setup

- `setup/nodes.json` - Defines 5 nodes, each with an initial proposed value and a unique node ID.
- `setup/network.json` - Defines which nodes can communicate with which (adjacency list), simulating network partitions.

## Protocol Rules

This is a simplified majority-vote consensus protocol:

1. **Each round**, every node sends its current value to all nodes it can communicate with.
2. Each node collects all values it receives (including its own).
3. Each node adopts the **majority value** among the values it received. If there is a tie, the node keeps its current value.
4. Consensus is reached when ALL nodes hold the same value.
5. Maximum of 10 rounds. If consensus is not reached by round 10, report failure.

## Task

1. Read `setup/nodes.json` and `setup/network.json`.
2. Simulate the consensus protocol round by round.
3. Write `setup/consensus.json` with the final result.
4. Write `setup/rounds_log.json` with the state of each node after every round.

## Output Format

`setup/consensus.json`:
```json
{
  "consensus_reached": true | false,
  "final_value": "<agreed value or null>",
  "rounds_needed": <number>,
  "final_node_states": {
    "<node_id>": "<value>",
    ...
  }
}
```

`setup/rounds_log.json`:
```json
{
  "rounds": [
    {
      "round": 1,
      "node_states": {
        "<node_id>": {
          "value": "<current value>",
          "received_values": ["<val1>", "<val2>", ...],
          "adopted": "<value adopted this round>"
        },
        ...
      }
    },
    ...
  ]
}
```

## Constraints

- Nodes can only communicate according to `network.json`. If node A cannot reach node B, it does not receive B's value.
- Communication is bidirectional: if A can reach B, then B can reach A.
- A node always includes its own value in its received values.
- The network topology does NOT change between rounds.
