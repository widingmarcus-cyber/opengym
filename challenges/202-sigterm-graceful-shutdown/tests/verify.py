import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_completed_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "completed.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "completed_json", "passed": False, "message": "completed.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) != 5:
        print(json.dumps({"test": "completed_json", "passed": False,
                          "message": f"completed.json should have 5 tasks, got {len(data) if isinstance(data, list) else 'non-list'}"}))
        return
    expected_results = [
        {"task_id": 1, "result": 23},
        {"task_id": 2, "result": 30},
        {"task_id": 3, "result": 21},
        {"task_id": 4, "result": 12},
        {"task_id": 5, "result": 37}
    ]
    for i, exp in enumerate(expected_results):
        if data[i].get("task_id") != exp["task_id"] or data[i].get("result") != exp["result"]:
            print(json.dumps({"test": "completed_json", "passed": False,
                              "message": f"Task {exp['task_id']}: expected result={exp['result']}, got {data[i].get('result')}"}))
            return
    print(json.dumps({"test": "completed_json", "passed": True, "message": "First 5 tasks completed correctly"}))


def test_remaining_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "remaining.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "remaining_json", "passed": False, "message": "remaining.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) != 5:
        print(json.dumps({"test": "remaining_json", "passed": False,
                          "message": f"remaining.json should have 5 tasks, got {len(data) if isinstance(data, list) else 'non-list'}"}))
        return
    expected_ids = [6, 7, 8, 9, 10]
    actual_ids = [t.get("task_id") for t in data]
    if actual_ids != expected_ids:
        print(json.dumps({"test": "remaining_json", "passed": False,
                          "message": f"Remaining task IDs should be {expected_ids}, got {actual_ids}"}))
        return
    print(json.dumps({"test": "remaining_json", "passed": True, "message": "5 remaining tasks saved correctly"}))


def test_shutdown_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "shutdown_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "shutdown_report", "passed": False, "message": "shutdown_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    if report.get("tasks_completed") != 5:
        print(json.dumps({"test": "shutdown_report", "passed": False,
                          "message": f"tasks_completed should be 5, got {report.get('tasks_completed')}"}))
        return
    if report.get("tasks_remaining") != 5:
        print(json.dumps({"test": "shutdown_report", "passed": False,
                          "message": f"tasks_remaining should be 5, got {report.get('tasks_remaining')}"}))
        return
    if report.get("shutdown_reason") != "SIGTERM":
        print(json.dumps({"test": "shutdown_report", "passed": False,
                          "message": f"shutdown_reason should be 'SIGTERM', got '{report.get('shutdown_reason')}'"}))
        return
    if report.get("clean_shutdown") is not True:
        print(json.dumps({"test": "shutdown_report", "passed": False,
                          "message": f"clean_shutdown should be true, got {report.get('clean_shutdown')}"}))
        return
    print(json.dumps({"test": "shutdown_report", "passed": True, "message": "Shutdown report is valid"}))


def test_signal_handling_added():
    path = os.path.join(CHALLENGE_DIR, "setup", "worker.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "signal_handling", "passed": False, "message": "worker.py not found"}))
        return
    with open(path) as f:
        code = f.read()
    if "signal" not in code:
        print(json.dumps({"test": "signal_handling", "passed": False,
                          "message": "worker.py does not import or use the signal module"}))
        return
    if "SIGTERM" not in code and "SIGINT" not in code:
        print(json.dumps({"test": "signal_handling", "passed": False,
                          "message": "worker.py does not reference SIGTERM or SIGINT"}))
        return
    print(json.dumps({"test": "signal_handling", "passed": True, "message": "Signal handling code is present"}))


if __name__ == "__main__":
    test_completed_json()
    test_remaining_json()
    test_shutdown_report()
    test_signal_handling_added()
