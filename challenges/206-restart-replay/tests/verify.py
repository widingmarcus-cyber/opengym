import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_LEDGER = {
    "ACC001": 1250.0,
    "ACC002": 2700.0,
    "ACC003": 1550.0,
    "ACC004": 2900.0
}


def test_wal_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "wal.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "wal_exists", "passed": False, "message": "wal.json not found"}))
        return
    with open(path) as f:
        wal = json.load(f)
    if not isinstance(wal, list) or len(wal) != 6:
        print(json.dumps({"test": "wal_exists", "passed": False,
                          "message": f"WAL should have 6 entries, got {len(wal) if isinstance(wal, list) else 'non-list'}"}))
        return
    for i, entry in enumerate(wal):
        if entry.get("seq") != i + 1:
            print(json.dumps({"test": "wal_exists", "passed": False,
                              "message": f"WAL entry {i} should have seq={i+1}, got {entry.get('seq')}"}))
            return
    print(json.dumps({"test": "wal_exists", "passed": True, "message": "WAL has 6 sequenced entries"}))


def test_state_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "state_json", "passed": False, "message": "state.json not found"}))
        return
    with open(path) as f:
        state = json.load(f)
    ledger = state.get("ledger", {})
    for acc, expected_bal in EXPECTED_LEDGER.items():
        actual = ledger.get(acc)
        if actual != expected_bal:
            print(json.dumps({"test": "state_json", "passed": False,
                              "message": f"{acc} should have balance {expected_bal}, got {actual}"}))
            return
    if state.get("wal_length") != 6:
        print(json.dumps({"test": "state_json", "passed": False,
                          "message": f"wal_length should be 6, got {state.get('wal_length')}"}))
        return
    print(json.dumps({"test": "state_json", "passed": True, "message": "State ledger is correct"}))


def test_replay_result_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "replay_result.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "replay_result", "passed": False, "message": "replay_result.json not found"}))
        return False
    print(json.dumps({"test": "replay_result", "passed": True, "message": "replay_result.json exists"}))
    return True


def test_replay_result_values():
    path = os.path.join(CHALLENGE_DIR, "setup", "replay_result.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "replay_values", "passed": False, "message": "replay_result.json not found"}))
        return
    with open(path) as f:
        result = json.load(f)
    if result.get("replay_successful") is not True:
        print(json.dumps({"test": "replay_values", "passed": False,
                          "message": "replay_successful should be true"}))
        return
    if result.get("operations_replayed") != 6:
        print(json.dumps({"test": "replay_values", "passed": False,
                          "message": f"operations_replayed should be 6, got {result.get('operations_replayed')}"}))
        return
    if result.get("matches_saved_state") is not True:
        print(json.dumps({"test": "replay_values", "passed": False,
                          "message": "matches_saved_state should be true"}))
        return
    final = result.get("final_ledger", {})
    for acc, expected_bal in EXPECTED_LEDGER.items():
        if final.get(acc) != expected_bal:
            print(json.dumps({"test": "replay_values", "passed": False,
                              "message": f"Replayed {acc} should be {expected_bal}, got {final.get(acc)}"}))
            return
    print(json.dumps({"test": "replay_values", "passed": True, "message": "Replay result values are correct"}))


if __name__ == "__main__":
    test_wal_exists()
    test_state_json()
    test_replay_result_exists()
    test_replay_result_values()
