import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_answer_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.json not found"}))
        return False
    print(json.dumps({"test": "answer_exists", "passed": True, "message": "answer.json exists"}))
    return True


def test_deduplicated_count():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        deduped = data.get("deduplicated", [])
        if len(deduped) == 2:
            print(json.dumps({"test": "deduplicated_count", "passed": True, "message": "Deduplicated list has 2 entries"}))
            return True
        else:
            print(json.dumps({"test": "deduplicated_count", "passed": False, "message": f"Expected 2 entries, got {len(deduped)}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "deduplicated_count", "passed": False, "message": str(e)}))
        return False


def test_run2_removed():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        deduped = data.get("deduplicated", [])
        ids = [d.get("id") for d in deduped]
        if "run_2" not in ids and "run_1" in ids and "run_3" in ids:
            print(json.dumps({"test": "run2_removed", "passed": True, "message": "run_2 correctly removed, run_1 and run_3 kept"}))
            return True
        else:
            print(json.dumps({"test": "run2_removed", "passed": False, "message": f"Expected run_1 and run_3 kept, run_2 removed. Got ids: {ids}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "run2_removed", "passed": False, "message": str(e)}))
        return False


def test_duplicates_removed_count():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        count = data.get("duplicates_removed")
        if count == 1:
            print(json.dumps({"test": "duplicates_removed_count", "passed": True, "message": "Correctly reports 1 duplicate removed"}))
            return True
        else:
            print(json.dumps({"test": "duplicates_removed_count", "passed": False, "message": f"Expected duplicates_removed=1, got {count}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "duplicates_removed_count", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_deduplicated_count()
    test_run2_removed()
    test_duplicates_removed_count()
