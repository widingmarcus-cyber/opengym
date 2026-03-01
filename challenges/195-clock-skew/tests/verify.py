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


def test_max_skew():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        skew = data.get("max_skew_seconds")
        if skew == 10:
            print(json.dumps({"test": "max_skew", "passed": True, "message": "Correct max skew: 10 seconds"}))
            return True
        else:
            print(json.dumps({"test": "max_skew", "passed": False, "message": f"Expected max_skew_seconds=10, got {skew}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "max_skew", "passed": False, "message": str(e)}))
        return False


def test_within_tolerance():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("within_tolerance") is False:
            print(json.dumps({"test": "within_tolerance", "passed": True, "message": "Correctly determined skew is NOT within tolerance"}))
            return True
        else:
            print(json.dumps({"test": "within_tolerance", "passed": False, "message": "Expected within_tolerance=false"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "within_tolerance", "passed": False, "message": str(e)}))
        return False


def test_worst_pair():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        pair = sorted(data.get("worst_pair", []))
        if pair == ["node_b", "node_c"]:
            print(json.dumps({"test": "worst_pair", "passed": True, "message": "Correct worst pair: node_b and node_c"}))
            return True
        else:
            print(json.dumps({"test": "worst_pair", "passed": False, "message": f"Expected ['node_b', 'node_c'], got {pair}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "worst_pair", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_max_skew()
    test_within_tolerance()
    test_worst_pair()
