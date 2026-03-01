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


def test_retryable_tasks():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        retryable = sorted(data.get("retryable", []))
        if retryable == ["t1", "t3"]:
            print(json.dumps({"test": "retryable_tasks", "passed": True, "message": "Correctly identified t1 and t3 as retryable"}))
            return True
        else:
            print(json.dumps({"test": "retryable_tasks", "passed": False, "message": f"Expected ['t1', 't3'], got {retryable}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "retryable_tasks", "passed": False, "message": str(e)}))
        return False


def test_expired_tasks():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        expired = sorted(data.get("expired", []))
        if expired == ["t2"]:
            print(json.dumps({"test": "expired_tasks", "passed": True, "message": "Correctly identified t2 as expired"}))
            return True
        else:
            print(json.dumps({"test": "expired_tasks", "passed": False, "message": f"Expected ['t2'], got {expired}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "expired_tasks", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_retryable_tasks()
    test_expired_tasks()
