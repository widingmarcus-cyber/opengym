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


def test_three_events():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        if len(data) == 3:
            print(json.dumps({"test": "three_events", "passed": True, "message": "answer.json has 3 events"}))
            return True
        else:
            print(json.dumps({"test": "three_events", "passed": False, "message": f"Expected 3 events, got {len(data)}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "three_events", "passed": False, "message": str(e)}))
        return False


def test_meeting_utc():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        meeting = [e for e in data if e.get("event") == "meeting"]
        if not meeting:
            print(json.dumps({"test": "meeting_utc", "passed": False, "message": "meeting event not found"}))
            return False
        utc = meeting[0].get("utc_time", "")
        if "10:00:00" in utc and utc.endswith("Z"):
            print(json.dumps({"test": "meeting_utc", "passed": True, "message": "meeting correctly at 10:00 UTC"}))
            return True
        else:
            print(json.dumps({"test": "meeting_utc", "passed": False, "message": f"Expected meeting at 10:00:00Z, got {utc}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "meeting_utc", "passed": False, "message": str(e)}))
        return False


def test_deploy_utc():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        deploy = [e for e in data if e.get("event") == "deploy"]
        if not deploy:
            print(json.dumps({"test": "deploy_utc", "passed": False, "message": "deploy event not found"}))
            return False
        utc = deploy[0].get("utc_time", "")
        if "15:00:00" in utc and utc.endswith("Z"):
            print(json.dumps({"test": "deploy_utc", "passed": True, "message": "deploy correctly converted to 15:00 UTC"}))
            return True
        else:
            print(json.dumps({"test": "deploy_utc", "passed": False, "message": f"Expected deploy at 15:00:00Z, got {utc}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "deploy_utc", "passed": False, "message": str(e)}))
        return False


def test_standup_utc():
    path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
    try:
        with open(path) as f:
            data = json.load(f)
        standup = [e for e in data if e.get("event") == "standup"]
        if not standup:
            print(json.dumps({"test": "standup_utc", "passed": False, "message": "standup event not found"}))
            return False
        utc = standup[0].get("utc_time", "")
        if "01:00:00" in utc and utc.endswith("Z"):
            print(json.dumps({"test": "standup_utc", "passed": True, "message": "standup correctly converted to 01:00 UTC"}))
            return True
        else:
            print(json.dumps({"test": "standup_utc", "passed": False, "message": f"Expected standup at 01:00:00Z, got {utc}"}))
            return False
    except Exception as e:
        print(json.dumps({"test": "standup_utc", "passed": False, "message": str(e)}))
        return False


if __name__ == "__main__":
    test_answer_exists()
    test_three_events()
    test_meeting_utc()
    test_deploy_utc()
    test_standup_utc()
