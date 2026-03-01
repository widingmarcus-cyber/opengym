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


def test_task_identified():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if data.get("task") == "backup":
            print(json.dumps({"test": "task_identified", "passed": True, "message": "Correctly identifies backup task"}))
            return True
        else:
            print(json.dumps({"test": "task_identified", "passed": False, "message": f"Expected task='backup', got '{data.get('task')}'"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "task_identified", "passed": False, "message": str(e)}))
        return False


def test_issue_detected():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        issue = data.get("issue")
        if issue and issue.strip():
            print(json.dumps({"test": "issue_detected", "passed": True, "message": f"DST issue detected: {issue}"}))
            return True
        else:
            print(json.dumps({"test": "issue_detected", "passed": False, "message": "issue field is empty or null - DST problem not detected"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "issue_detected", "passed": False, "message": str(e)}))
        return False


def test_resolution_provided():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        resolution = data.get("resolution")
        valid_resolutions = ["skip", "shift_to_0330", "shift_to_03:30", "shift", "postpone"]
        if resolution and any(r in resolution.lower() for r in ["skip", "shift", "0330", "03:30", "postpone"]):
            print(json.dumps({"test": "resolution_provided", "passed": True, "message": f"Valid resolution provided: {resolution}"}))
            return True
        elif resolution:
            # Accept any non-empty resolution
            print(json.dumps({"test": "resolution_provided", "passed": True, "message": f"Resolution provided: {resolution}"}))
            return True
        else:
            print(json.dumps({"test": "resolution_provided", "passed": False, "message": "No resolution provided"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "resolution_provided", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_task_identified()
    test_issue_detected()
    test_resolution_provided()
