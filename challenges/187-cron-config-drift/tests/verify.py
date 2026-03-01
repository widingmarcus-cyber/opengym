import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_drift_report_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "drift_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "drift_report_exists", "passed": False, "message": "setup/drift_report.json not found"}))
        return False
    print(json.dumps({"test": "drift_report_exists", "passed": True, "message": "drift_report.json exists"}))
    return True


def test_drift_report_has_baseline():
    path = os.path.join(CHALLENGE_DIR, "setup", "drift_report.json")
    try:
        with open(path) as f:
            data = json.load(f)
        baseline = data.get("baseline")
        if baseline is None:
            print(json.dumps({"test": "drift_report_has_baseline", "passed": False, "message": "No baseline found in drift_report.json"}))
            return False
        tasks = baseline.get("tasks", [])
        sync_task = [t for t in tasks if t.get("name") == "sync"]
        if sync_task and sync_task[0].get("interval") == "daily":
            print(json.dumps({"test": "drift_report_has_baseline", "passed": True, "message": "Baseline correctly records sync as daily"}))
            return True
        else:
            print(json.dumps({"test": "drift_report_has_baseline", "passed": False, "message": "Baseline does not correctly record sync interval as daily"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "drift_report_has_baseline", "passed": False, "message": str(e)}))
        return False


def test_answer_json_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_json_exists", "passed": False, "message": "setup/answer.json not found"}))
        return False
    print(json.dumps({"test": "answer_json_exists", "passed": True, "message": "answer.json exists"}))
    return True


def test_drift_detected():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("drifted") is True:
            print(json.dumps({"test": "drift_detected", "passed": True, "message": "Drift correctly detected"}))
            return True
        else:
            print(json.dumps({"test": "drift_detected", "passed": False, "message": "Drift not detected, expected drifted=true"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "drift_detected", "passed": False, "message": str(e)}))
        return False


def test_correct_changes():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        changes = data.get("changes", [])
        if len(changes) != 1:
            print(json.dumps({"test": "correct_changes", "passed": False, "message": f"Expected 1 change, found {len(changes)}"}))
            return False
        change = changes[0]
        if (change.get("task") == "sync" and
                change.get("field") == "interval" and
                change.get("from") == "daily" and
                change.get("to") == "weekly"):
            print(json.dumps({"test": "correct_changes", "passed": True, "message": "Correct change detected: sync interval daily->weekly"}))
            return True
        else:
            print(json.dumps({"test": "correct_changes", "passed": False, "message": f"Incorrect change details: {change}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "correct_changes", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_drift_report_exists()
    test_drift_report_has_baseline()
    test_answer_json_exists()
    test_drift_detected()
    test_correct_changes()
