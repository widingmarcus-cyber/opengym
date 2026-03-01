import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Expected result for the given configuration:
# Initial: A=alpha, B=beta, C=alpha, D=beta, E=alpha
# Network: nearly fully connected (B missing E link, E missing B link)
# Round 1: A=alpha, B=beta, C=alpha, D=alpha, E=alpha (D flips from beta to alpha)
# Round 2: All alpha (B flips from beta to alpha)
# Consensus reached in 2 rounds on value "alpha"

EXPECTED_CONSENSUS = True
EXPECTED_VALUE = "alpha"
EXPECTED_ROUNDS = 2

def test_consensus_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "consensus.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "consensus_exists", "passed": False, "message": "consensus.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "consensus_exists", "passed": True, "message": "consensus.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "consensus_exists", "passed": False, "message": "consensus.json is not valid JSON"}))
        return None

def test_consensus_reached(data):
    if data is None:
        print(json.dumps({"test": "consensus_reached", "passed": False, "message": "No data to check"}))
        return
    if data.get("consensus_reached") != EXPECTED_CONSENSUS:
        print(json.dumps({"test": "consensus_reached", "passed": False, "message": f"consensus_reached should be {EXPECTED_CONSENSUS}, got {data.get('consensus_reached')}"}))
        return
    if data.get("final_value") != EXPECTED_VALUE:
        print(json.dumps({"test": "consensus_reached", "passed": False, "message": f"final_value should be '{EXPECTED_VALUE}', got '{data.get('final_value')}'"}))
        return
    if data.get("rounds_needed") != EXPECTED_ROUNDS:
        print(json.dumps({"test": "consensus_reached", "passed": False, "message": f"rounds_needed should be {EXPECTED_ROUNDS}, got {data.get('rounds_needed')}"}))
        return
    print(json.dumps({"test": "consensus_reached", "passed": True, "message": f"Consensus correctly reached on '{EXPECTED_VALUE}' in {EXPECTED_ROUNDS} rounds"}))

def test_final_node_states(data):
    if data is None:
        print(json.dumps({"test": "final_node_states", "passed": False, "message": "No data to check"}))
        return
    states = data.get("final_node_states", {})
    expected_nodes = {"node-A", "node-B", "node-C", "node-D", "node-E"}
    if set(states.keys()) != expected_nodes:
        print(json.dumps({"test": "final_node_states", "passed": False, "message": f"Expected nodes {expected_nodes}, got {set(states.keys())}"}))
        return
    for node, value in states.items():
        if value != EXPECTED_VALUE:
            print(json.dumps({"test": "final_node_states", "passed": False, "message": f"{node} should have value '{EXPECTED_VALUE}', got '{value}'"}))
            return
    print(json.dumps({"test": "final_node_states", "passed": True, "message": "All nodes have the consensus value 'alpha'"}))

def test_rounds_log_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "rounds_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "rounds_log_exists", "passed": False, "message": "rounds_log.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "rounds_log_exists", "passed": True, "message": "rounds_log.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "rounds_log_exists", "passed": False, "message": "rounds_log.json is not valid JSON"}))
        return None

def test_rounds_log_detail(log_data):
    if log_data is None:
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": "No rounds log data"}))
        return
    rounds = log_data.get("rounds", [])
    if len(rounds) != EXPECTED_ROUNDS:
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": f"Expected {EXPECTED_ROUNDS} rounds in log, got {len(rounds)}"}))
        return
    # Check round 1: D should flip from beta to alpha
    r1 = rounds[0]
    if r1.get("round") != 1:
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": "First round should be numbered 1"}))
        return
    r1_states = r1.get("node_states", {})
    if "node-D" not in r1_states:
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": "node-D missing from round 1 states"}))
        return
    d_adopted = r1_states["node-D"].get("adopted", r1_states["node-D"].get("value"))
    if d_adopted != "alpha":
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": f"In round 1, node-D should adopt 'alpha', got '{d_adopted}'"}))
        return
    # B should still be beta after round 1
    b_adopted = r1_states.get("node-B", {}).get("adopted", r1_states.get("node-B", {}).get("value"))
    if b_adopted != "beta":
        print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": f"In round 1, node-B should keep 'beta', got '{b_adopted}'"}))
        return
    # Check that each node has received_values
    for node_id, node_state in r1_states.items():
        if "received_values" not in node_state:
            print(json.dumps({"test": "rounds_log_detail", "passed": False, "message": f"Round 1 {node_id} missing received_values"}))
            return
    print(json.dumps({"test": "rounds_log_detail", "passed": True, "message": "Rounds log has correct detail: D flips in round 1, B flips in round 2"}))

def test_received_values_match_topology(log_data):
    if log_data is None:
        print(json.dumps({"test": "topology_consistency", "passed": False, "message": "No rounds log data"}))
        return
    net_path = os.path.join(CHALLENGE_DIR, "setup", "network.json")
    with open(net_path) as f:
        network = json.load(f)
    topology = network["topology"]
    rounds = log_data.get("rounds", [])
    if not rounds:
        print(json.dumps({"test": "topology_consistency", "passed": False, "message": "No rounds in log"}))
        return
    # Check round 1: each node should receive values from its neighbors + itself
    r1 = rounds[0]
    r1_states = r1.get("node_states", {})
    for node_id, node_state in r1_states.items():
        received = node_state.get("received_values", [])
        expected_count = len(topology.get(node_id, [])) + 1  # neighbors + self
        if len(received) != expected_count:
            print(json.dumps({"test": "topology_consistency", "passed": False, "message": f"{node_id} should receive {expected_count} values (self + {len(topology.get(node_id, []))} neighbors), got {len(received)}"}))
            return
    print(json.dumps({"test": "topology_consistency", "passed": True, "message": "Received values count matches network topology for all nodes"}))

if __name__ == "__main__":
    data = test_consensus_exists()
    test_consensus_reached(data)
    test_final_node_states(data)
    log_data = test_rounds_log_exists()
    test_rounds_log_detail(log_data)
    test_received_values_match_topology(log_data)
