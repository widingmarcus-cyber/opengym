import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_results_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "results.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "results_exists", "passed": False, "message": "setup/results.json not found"}))
        return False
    print(json.dumps({"test": "results_exists", "passed": True, "message": "results.json exists"}))
    return True


def test_results_has_four_entries():
    path = os.path.join(CHALLENGE_DIR, "setup", "results.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if len(data) == 4:
            print(json.dumps({"test": "results_has_four_entries", "passed": True, "message": "results.json has 4 entries"}))
            return True
        else:
            print(json.dumps({"test": "results_has_four_entries", "passed": False, "message": f"Expected 4 entries, got {len(data)}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "results_has_four_entries", "passed": False, "message": str(e)}))
        return False


def test_task3_not_executed():
    path = os.path.join(CHALLENGE_DIR, "setup", "results.json")
    try:
        with open(path) as f:
            data = json.load(f)
        task3 = [r for r in data if r.get("id") == 3]
        if not task3:
            print(json.dumps({"test": "task3_not_executed", "passed": False, "message": "Task 3 not found in results"}))
            return False
        t3 = task3[0]
        if t3.get("executed") is False and t3.get("reason") == "cancelled":
            print(json.dumps({"test": "task3_not_executed", "passed": True, "message": "Task 3 correctly not executed with reason=cancelled"}))
            return True
        else:
            print(json.dumps({"test": "task3_not_executed", "passed": False, "message": f"Task 3 should have executed=false and reason=cancelled, got {t3}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "task3_not_executed", "passed": False, "message": str(e)}))
        return False


def test_other_tasks_executed():
    path = os.path.join(CHALLENGE_DIR, "setup", "results.json")
    try:
        with open(path) as f:
            data = json.load(f)
        executed_ids = [r["id"] for r in data if r.get("executed") is True]
        if sorted(executed_ids) == [1, 2, 4]:
            print(json.dumps({"test": "other_tasks_executed", "passed": True, "message": "Tasks 1, 2, 4 correctly executed"}))
            return True
        else:
            print(json.dumps({"test": "other_tasks_executed", "passed": False, "message": f"Expected tasks [1, 2, 4] executed, got {sorted(executed_ids)}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "other_tasks_executed", "passed": False, "message": str(e)}))
        return False


def test_answer_txt():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_txt", "passed": False, "message": "setup/answer.txt not found"}))
        return False
    try:
        with open(path) as f:
            content = f.read().strip()
        if content == "3":
            print(json.dumps({"test": "answer_txt", "passed": True, "message": "answer.txt correctly contains '3'"}))
            return True
        else:
            print(json.dumps({"test": "answer_txt", "passed": False, "message": f"Expected '3', got '{content}'"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "answer_txt", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_results_exists()
    test_results_has_four_entries()
    test_task3_not_executed()
    test_other_tasks_executed()
    test_answer_txt()
