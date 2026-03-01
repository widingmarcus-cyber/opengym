import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_execution_log_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "execution_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "execution_log_exists", "passed": False, "message": "setup/execution_log.json not found"}))
        return False
    print(json.dumps({"test": "execution_log_exists", "passed": True, "message": "execution_log.json exists"}))
    return True


def test_execution_log_has_runs():
    path = os.path.join(CHALLENGE_DIR, "setup", "execution_log.json")
    try:
        with open(path) as f:
            data = json.load(f)
        runs = data.get("runs", [])
        if len(runs) >= 2:
            print(json.dumps({"test": "execution_log_has_runs", "passed": True, "message": "execution_log.json has at least 2 runs"}))
            return True
        else:
            print(json.dumps({"test": "execution_log_has_runs", "passed": False, "message": f"Expected at least 2 runs, found {len(runs)}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "execution_log_has_runs", "passed": False, "message": str(e)}))
        return False


def test_fresh_policy_enforcement():
    path = os.path.join(CHALLENGE_DIR, "setup", "execution_log.json")
    try:
        with open(path) as f:
            data = json.load(f)
        runs = data.get("runs", [])
        all_ok = True
        for run in runs:
            for ex in run.get("executions", []):
                if ex.get("policy") == "fresh":
                    ctx = ex.get("context", "")
                    if ctx != "clean":
                        all_ok = False
        if all_ok:
            print(json.dumps({"test": "fresh_policy_enforcement", "passed": True, "message": "All fresh tasks have clean context"}))
        else:
            print(json.dumps({"test": "fresh_policy_enforcement", "passed": False, "message": "Some fresh tasks do not have clean context"}))
        return all_ok
    except Exception as e:
        print(json.dumps({"test": "fresh_policy_enforcement", "passed": False, "message": str(e)}))
        return False


def test_reuse_policy_enforcement():
    path = os.path.join(CHALLENGE_DIR, "setup", "execution_log.json")
    try:
        with open(path) as f:
            data = json.load(f)
        runs = data.get("runs", [])
        if len(runs) < 2:
            print(json.dumps({"test": "reuse_policy_enforcement", "passed": False, "message": "Need at least 2 runs to verify reuse"}))
            return False
        # In run 2, reuse tasks should have reused context
        run2 = runs[1]
        reuse_ok = True
        for ex in run2.get("executions", []):
            if ex.get("policy") == "reuse":
                ctx = ex.get("context", "")
                if "reuse" not in ctx.lower() and "existing" not in ctx.lower():
                    reuse_ok = False
        if reuse_ok:
            print(json.dumps({"test": "reuse_policy_enforcement", "passed": True, "message": "Reuse tasks properly reuse context in run 2"}))
        else:
            print(json.dumps({"test": "reuse_policy_enforcement", "passed": False, "message": "Reuse tasks did not reuse context in run 2"}))
        return reuse_ok
    except Exception as e:
        print(json.dumps({"test": "reuse_policy_enforcement", "passed": False, "message": str(e)}))
        return False


def test_answer_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "answer_json", "passed": False, "message": "setup/answer.json not found"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        fresh = data.get("fresh_count")
        reuse = data.get("reuse_count")
        if fresh == 4 and reuse == 2:
            print(json.dumps({"test": "answer_json", "passed": True, "message": "Correct counts: fresh=4, reuse=2"}))
            return True
        else:
            print(json.dumps({"test": "answer_json", "passed": False, "message": f"Expected fresh=4, reuse=2 but got fresh={fresh}, reuse={reuse}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "answer_json", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_execution_log_exists()
    test_execution_log_has_runs()
    test_fresh_policy_enforcement()
    test_reuse_policy_enforcement()
    test_answer_json()
