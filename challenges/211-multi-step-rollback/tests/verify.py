import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_rolled_back_state_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "rolled_back_exists", "passed": False,
                          "message": "rolled_back_state.json not found"}))
        return
    print(json.dumps({"test": "rolled_back_exists", "passed": True,
                      "message": "rolled_back_state.json exists"}))


def test_matches_original():
    rb_path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    orig_path = os.path.join(CHALLENGE_DIR, "setup", "original_state.json")
    if not os.path.exists(rb_path):
        print(json.dumps({"test": "matches_original", "passed": False,
                          "message": "rolled_back_state.json not found"}))
        return
    with open(rb_path) as f:
        rolled_back = json.load(f)
    with open(orig_path) as f:
        original = json.load(f)
    if rolled_back != original:
        # Find first difference
        for key in original:
            if rolled_back.get(key) != original[key]:
                print(json.dumps({"test": "matches_original", "passed": False,
                                  "message": f"Mismatch at '{key}': expected {original[key]}, got {rolled_back.get(key)}"}))
                return
        print(json.dumps({"test": "matches_original", "passed": False,
                          "message": "States differ (extra keys in rolled back state)"}))
        return
    print(json.dumps({"test": "matches_original", "passed": True,
                      "message": "Rolled-back state matches original exactly"}))


def test_database_version_reverted():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "db_version", "passed": False, "message": "rolled_back_state.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("database_version") != "v3.2.0":
        print(json.dumps({"test": "db_version", "passed": False,
                          "message": f"database_version should be 'v3.2.0', got '{data.get('database_version')}'"}))
        return
    print(json.dumps({"test": "db_version", "passed": True,
                      "message": "Database version reverted to v3.2.0"}))


def test_schema_reverted():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "schema_reverted", "passed": False, "message": "rolled_back_state.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    columns = data.get("schema", {}).get("users", {}).get("columns", [])
    if "phone" in columns:
        print(json.dumps({"test": "schema_reverted", "passed": False,
                          "message": "users.columns still contains 'phone' — should have been removed"}))
        return
    if columns != ["id", "name", "email"]:
        print(json.dumps({"test": "schema_reverted", "passed": False,
                          "message": f"users.columns should be ['id','name','email'], got {columns}"}))
        return
    print(json.dumps({"test": "schema_reverted", "passed": True,
                      "message": "Schema reverted (phone column removed)"}))


def test_rollback_log():
    path = os.path.join(CHALLENGE_DIR, "setup", "rollback_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "rollback_log", "passed": False, "message": "rollback_log.json not found"}))
        return
    with open(path) as f:
        log = json.load(f)
    if log.get("steps_rolled_back") != [4, 3, 2, 1]:
        print(json.dumps({"test": "rollback_log", "passed": False,
                          "message": f"steps_rolled_back should be [4,3,2,1], got {log.get('steps_rolled_back')}"}))
        return
    if log.get("all_reverted") is not True:
        print(json.dumps({"test": "rollback_log", "passed": False,
                          "message": "all_reverted should be true"}))
        return
    if log.get("final_matches_original") is not True:
        print(json.dumps({"test": "rollback_log", "passed": False,
                          "message": "final_matches_original should be true"}))
        return
    print(json.dumps({"test": "rollback_log", "passed": True, "message": "Rollback log is valid"}))


if __name__ == "__main__":
    test_rolled_back_state_exists()
    test_matches_original()
    test_database_version_reverted()
    test_schema_reverted()
    test_rollback_log()
