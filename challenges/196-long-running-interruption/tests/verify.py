import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_progress_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "progress.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "progress_exists", "passed": False, "message": "setup/progress.json not found"}))
        return False
    print(json.dumps({"test": "progress_exists", "passed": True, "message": "progress.json exists"}))
    return True


def test_all_items_completed():
    path = os.path.join(CHALLENGE_DIR, "setup", "progress.json")
    try:
        with open(path) as f:
            data = json.load(f)
        completed = sorted(data.get("completed", []))
        if completed == list(range(1, 11)):
            print(json.dumps({"test": "all_items_completed", "passed": True, "message": "All 10 items completed"}))
            return True
        else:
            print(json.dumps({"test": "all_items_completed", "passed": False, "message": f"Expected items 1-10 completed, got {completed}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "all_items_completed", "passed": False, "message": str(e)}))
        return False


def test_no_remaining():
    path = os.path.join(CHALLENGE_DIR, "setup", "progress.json")
    try:
        with open(path) as f:
            data = json.load(f)
        remaining = data.get("remaining", [])
        if len(remaining) == 0:
            print(json.dumps({"test": "no_remaining", "passed": True, "message": "No remaining items"}))
            return True
        else:
            print(json.dumps({"test": "no_remaining", "passed": False, "message": f"Expected no remaining items, got {remaining}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "no_remaining", "passed": False, "message": str(e)}))
        return False


def test_answer_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.json not found"}))
        return False
    print(json.dumps({"test": "answer_exists", "passed": True, "message": "answer.json exists"}))
    return True


def test_answer_total_completed():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("total_completed") == 10:
            print(json.dumps({"test": "answer_total_completed", "passed": True, "message": "Correct total_completed: 10"}))
            return True
        else:
            print(json.dumps({"test": "answer_total_completed", "passed": False, "message": f"Expected total_completed=10, got {data.get('total_completed')}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "answer_total_completed", "passed": False, "message": str(e)}))
        return False


def test_answer_resumed_from():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("resumed_from") == 8:
            print(json.dumps({"test": "answer_resumed_from", "passed": True, "message": "Correct resumed_from: 8"}))
            return True
        else:
            print(json.dumps({"test": "answer_resumed_from", "passed": False, "message": f"Expected resumed_from=8, got {data.get('resumed_from')}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "answer_resumed_from", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_progress_exists()
    test_all_items_completed()
    test_no_remaining()
    test_answer_exists()
    test_answer_total_completed()
    test_answer_resumed_from()
