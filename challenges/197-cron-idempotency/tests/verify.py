import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_state_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "state_exists", "passed": False, "message": "setup/state.json not found"}))
        return False
    print(json.dumps({"test": "state_exists", "passed": True, "message": "state.json exists"}))
    return True


def test_run_count_is_one():
    path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    try:
        with open(path) as f:
            data = json.load(f)
        count = data.get("run_count")
        if count == 1:
            print(json.dumps({"test": "run_count_is_one", "passed": True, "message": "run_count correctly stayed at 1 (idempotent)"}))
            return True
        else:
            print(json.dumps({"test": "run_count_is_one", "passed": False, "message": f"Expected run_count=1, got {count}. Task was not idempotent."}))
            return False
    except Exception as e:
        print(json.dumps({"test": "run_count_is_one", "passed": False, "message": str(e)}))
        return False


def test_report_generated():
    path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("report_generated") is True:
            print(json.dumps({"test": "report_generated", "passed": True, "message": "report_generated is true"}))
            return True
        else:
            print(json.dumps({"test": "report_generated", "passed": False, "message": "Expected report_generated=true"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "report_generated", "passed": False, "message": str(e)}))
        return False


def test_run_log_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "run_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "run_log_exists", "passed": False, "message": "setup/run_log.json not found"}))
        return False
    print(json.dumps({"test": "run_log_exists", "passed": True, "message": "run_log.json exists"}))
    return True


def test_answer_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.json not found"}))
        return False
    print(json.dumps({"test": "answer_exists", "passed": True, "message": "answer.json exists"}))
    return True


def test_answer_idempotent():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        idempotent = data.get("idempotent")
        actual_runs = data.get("actual_runs")
        if idempotent is True and actual_runs == 1:
            print(json.dumps({"test": "answer_idempotent", "passed": True, "message": "Correct: idempotent=true, actual_runs=1"}))
            return True
        else:
            print(json.dumps({"test": "answer_idempotent", "passed": False, "message": f"Expected idempotent=true, actual_runs=1, got idempotent={idempotent}, actual_runs={actual_runs}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "answer_idempotent", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_state_exists()
    test_run_count_is_one()
    test_report_generated()
    test_run_log_exists()
    test_answer_exists()
    test_answer_idempotent()
