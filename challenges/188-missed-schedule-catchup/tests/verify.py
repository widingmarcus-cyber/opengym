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


def test_missed_hours():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        missed = data.get("missed", [])
        if sorted(missed) == [3, 4]:
            print(json.dumps({"test": "missed_hours", "passed": True, "message": "Correctly identified missed hours: [3, 4]"}))
            return True
        else:
            print(json.dumps({"test": "missed_hours", "passed": False, "message": f"Expected missed=[3, 4], got {missed}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "missed_hours", "passed": False, "message": str(e)}))
        return False


def test_catch_up_needed():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("catch_up_needed") is True:
            print(json.dumps({"test": "catch_up_needed", "passed": True, "message": "Correctly identified catch-up is needed"}))
            return True
        else:
            print(json.dumps({"test": "catch_up_needed", "passed": False, "message": "Expected catch_up_needed=true"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "catch_up_needed", "passed": False, "message": str(e)}))
        return False


def test_total_counts():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        scheduled = data.get("total_scheduled")
        executed = data.get("total_executed")
        if scheduled == 5 and executed == 3:
            print(json.dumps({"test": "total_counts", "passed": True, "message": "Correct counts: scheduled=5, executed=3"}))
            return True
        else:
            print(json.dumps({"test": "total_counts", "passed": False, "message": f"Expected scheduled=5, executed=3, got scheduled={scheduled}, executed={executed}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "total_counts", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_missed_hours()
    test_catch_up_needed()
    test_total_counts()
