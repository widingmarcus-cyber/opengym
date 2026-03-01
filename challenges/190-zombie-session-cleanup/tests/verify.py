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


def test_zombies_found():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        count = data.get("zombies_found")
        if count == 2:
            print(json.dumps({"test": "zombies_found", "passed": True, "message": "Correctly found 2 zombie sessions"}))
            return True
        else:
            print(json.dumps({"test": "zombies_found", "passed": False, "message": f"Expected 2 zombies, got {count}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "zombies_found", "passed": False, "message": str(e)}))
        return False


def test_terminated_ids():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        terminated = sorted(data.get("terminated", []))
        if terminated == ["s2", "s4"]:
            print(json.dumps({"test": "terminated_ids", "passed": True, "message": "Correctly identified s2 and s4 as zombies"}))
            return True
        else:
            print(json.dumps({"test": "terminated_ids", "passed": False, "message": f"Expected ['s2', 's4'], got {terminated}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "terminated_ids", "passed": False, "message": str(e)}))
        return False


def test_sessions_updated():
    path = os.path.join(CHALLENGE_DIR, "setup", "sessions.json")
    try:
        with open(path) as f:
            data = json.load(f)
        session_map = {s["id"]: s["status"] for s in data}
        s2_ok = session_map.get("s2") == "terminated"
        s4_ok = session_map.get("s4") == "terminated"
        s1_ok = session_map.get("s1") == "completed"
        s3_ok = session_map.get("s3") == "completed"
        if s2_ok and s4_ok and s1_ok and s3_ok:
            print(json.dumps({"test": "sessions_updated", "passed": True, "message": "sessions.json correctly updated: s2 and s4 terminated, s1 and s3 unchanged"}))
            return True
        else:
            print(json.dumps({"test": "sessions_updated", "passed": False, "message": f"Session statuses incorrect: {session_map}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "sessions_updated", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_zombies_found()
    test_terminated_ids()
    test_sessions_updated()
