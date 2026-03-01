import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_SUMS = {
    1: 543, 2: 827, 3: 304, 4: 530, 5: 582,
    6: 590, 7: 499, 8: 637, 9: 516, 10: 566,
    11: 661, 12: 657, 13: 413, 14: 611, 15: 515,
    16: 578, 17: 413, 18: 380, 19: 619, 20: 639
}


def test_checkpoint_10():
    path = os.path.join(CHALLENGE_DIR, "setup", "checkpoints", "checkpoint_10.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "checkpoint_10", "passed": False, "message": "checkpoint_10.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) != 10:
        print(json.dumps({"test": "checkpoint_10", "passed": False,
                          "message": f"checkpoint_10 should have 10 entries, got {len(data) if isinstance(data, list) else 'non-list'}"}))
        return
    for entry in data:
        bid = entry.get("batch_id")
        if bid and EXPECTED_SUMS.get(bid) != entry.get("sum"):
            print(json.dumps({"test": "checkpoint_10", "passed": False,
                              "message": f"Batch {bid} sum should be {EXPECTED_SUMS.get(bid)}, got {entry.get('sum')}"}))
            return
    print(json.dumps({"test": "checkpoint_10", "passed": True, "message": "Checkpoint 10 is correct"}))


def test_progress_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "progress.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "progress_json", "passed": False, "message": "progress.json not found"}))
        return
    with open(path) as f:
        prog = json.load(f)
    if prog.get("last_valid_checkpoint") != 10:
        print(json.dumps({"test": "progress_json", "passed": False,
                          "message": f"last_valid_checkpoint should be 10, got {prog.get('last_valid_checkpoint')}"}))
        return
    if prog.get("total_batches") != 20:
        print(json.dumps({"test": "progress_json", "passed": False,
                          "message": f"total_batches should be 20, got {prog.get('total_batches')}"}))
        return
    print(json.dumps({"test": "progress_json", "passed": True, "message": "progress.json is correct"}))


def test_final_results():
    path = os.path.join(CHALLENGE_DIR, "setup", "final_results.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "final_results", "passed": False, "message": "final_results.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    results = data.get("results", [])
    if len(results) != 20:
        print(json.dumps({"test": "final_results", "passed": False,
                          "message": f"Should have 20 results, got {len(results)}"}))
        return
    for entry in results:
        bid = entry.get("batch_id")
        expected = EXPECTED_SUMS.get(bid)
        if expected is None or entry.get("sum") != expected:
            print(json.dumps({"test": "final_results", "passed": False,
                              "message": f"Batch {bid} sum should be {expected}, got {entry.get('sum')}"}))
            return
    if data.get("all_complete") is not True:
        print(json.dumps({"test": "final_results", "passed": False,
                          "message": "all_complete should be true"}))
        return
    print(json.dumps({"test": "final_results", "passed": True, "message": "All 20 batch results correct"}))


def test_checkpoint_20():
    path = os.path.join(CHALLENGE_DIR, "setup", "checkpoints", "checkpoint_20.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "checkpoint_20", "passed": False, "message": "checkpoint_20.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) != 20:
        print(json.dumps({"test": "checkpoint_20", "passed": False,
                          "message": f"checkpoint_20 should have 20 entries, got {len(data) if isinstance(data, list) else 'non-list'}"}))
        return
    print(json.dumps({"test": "checkpoint_20", "passed": True, "message": "Final checkpoint has all 20 entries"}))


if __name__ == "__main__":
    test_checkpoint_10()
    test_progress_json()
    test_final_results()
    test_checkpoint_20()
