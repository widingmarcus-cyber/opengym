import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_FINAL_STATE = [22, 31, 42]


def test_replay_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "replay_output.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "replay_output_exists", "passed": False, "message": "replay_output.json not found"}))
        return
    print(json.dumps({"test": "replay_output_exists", "passed": True, "message": "replay_output.json exists"}))


def test_replay_output_deterministic():
    path = os.path.join(CHALLENGE_DIR, "setup", "replay_output.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "replay_deterministic", "passed": False, "message": "replay_output.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    # Check final state matches expected
    final_entry = data[-1]
    if final_entry.get("state") != EXPECTED_FINAL_STATE:
        print(json.dumps({"test": "replay_deterministic", "passed": False,
                          "message": f"Final state should be {EXPECTED_FINAL_STATE}, got {final_entry.get('state')}"}))
        return
    # Check timestamps use fixed values, not live timestamps
    for entry in data:
        ts = entry.get("timestamp", "")
        if "2026-02-28T10:00:" not in ts:
            print(json.dumps({"test": "replay_deterministic", "passed": False,
                              "message": f"Entry seq={entry.get('seq')} has non-fixed timestamp: {ts}"}))
            return
    print(json.dumps({"test": "replay_deterministic", "passed": True, "message": "Replay output is deterministic"}))


def test_outputs_match():
    path1 = os.path.join(CHALLENGE_DIR, "setup", "replay_output.json")
    path2 = os.path.join(CHALLENGE_DIR, "setup", "replay_output_2.json")
    if not os.path.exists(path1) or not os.path.exists(path2):
        print(json.dumps({"test": "outputs_match", "passed": False,
                          "message": "Need both replay_output.json and replay_output_2.json"}))
        return
    with open(path1) as f:
        data1 = json.load(f)
    with open(path2) as f:
        data2 = json.load(f)
    if data1 != data2:
        print(json.dumps({"test": "outputs_match", "passed": False,
                          "message": "replay_output.json and replay_output_2.json differ — replay is not deterministic"}))
        return
    print(json.dumps({"test": "outputs_match", "passed": True, "message": "Both replay outputs are identical"}))


def test_replayer_fixed():
    path = os.path.join(CHALLENGE_DIR, "setup", "replayer.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "replayer_fixed", "passed": False, "message": "replayer.py not found"}))
        return
    with open(path) as f:
        code = f.read()
    if "datetime.now()" in code:
        print(json.dumps({"test": "replayer_fixed", "passed": False,
                          "message": "replayer.py still uses datetime.now() — not deterministic"}))
        return
    if "random.seed" not in code and "seed" not in code.split("random.")[0]:
        print(json.dumps({"test": "replayer_fixed", "passed": False,
                          "message": "replayer.py does not seed the RNG from log entries"}))
        return
    print(json.dumps({"test": "replayer_fixed", "passed": True, "message": "Replayer has been fixed for determinism"}))


def test_determinism_proof():
    path = os.path.join(CHALLENGE_DIR, "setup", "determinism_proof.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "determinism_proof", "passed": False, "message": "determinism_proof.json not found"}))
        return
    with open(path) as f:
        proof = json.load(f)
    if proof.get("outputs_match") is not True:
        print(json.dumps({"test": "determinism_proof", "passed": False,
                          "message": "outputs_match should be true"}))
        return
    if proof.get("operations_replayed") != 5:
        print(json.dumps({"test": "determinism_proof", "passed": False,
                          "message": f"operations_replayed should be 5, got {proof.get('operations_replayed')}"}))
        return
    print(json.dumps({"test": "determinism_proof", "passed": True, "message": "Determinism proof is valid"}))


if __name__ == "__main__":
    test_replay_output_exists()
    test_replay_output_deterministic()
    test_outputs_match()
    test_replayer_fixed()
    test_determinism_proof()
