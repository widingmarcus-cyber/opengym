import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _compute_expected_state():
    """Compute the expected rolled-back state by applying rollback operations."""
    with open(os.path.join(CHALLENGE_DIR, "setup", "current_state.json")) as f:
        state = json.load(f)
    with open(os.path.join(CHALLENGE_DIR, "setup", "deployment_log.json")) as f:
        log = json.load(f)

    # Apply rollbacks in reverse order for completed steps
    completed = [s for s in log if s.get("status") == "completed"]
    completed.sort(key=lambda s: s["step"], reverse=True)

    for step in completed:
        rb = step.get("rollback", {})
        rb_type = rb.get("type")

        if rb_type == "set_field":
            path = rb["path"]
            parts = path.split(".")
            obj = state
            for p in parts[:-1]:
                obj = obj[p]
            obj[parts[-1]] = rb["value"]

        elif rb_type == "set_fields":
            for change in rb["changes"]:
                path = change["path"]
                parts = path.split(".")
                obj = state
                for p in parts[:-1]:
                    obj = obj[p]
                obj[parts[-1]] = change["value"]

        elif rb_type == "remove_from_list":
            path = rb["path"]
            parts = path.split(".")
            obj = state
            for p in parts[:-1]:
                obj = obj[p]
            lst = obj[parts[-1]]
            if rb["value"] in lst:
                lst.remove(rb["value"])

    return state


def test_rolled_back_state_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "rolled_back_exists", "passed": False,
                          "message": "rolled_back_state.json not found"}))
        return
    print(json.dumps({"test": "rolled_back_exists", "passed": True,
                      "message": "rolled_back_state.json exists"}))


def test_matches_expected():
    rb_path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(rb_path):
        print(json.dumps({"test": "matches_expected", "passed": False,
                          "message": "rolled_back_state.json not found"}))
        return
    with open(rb_path) as f:
        rolled_back = json.load(f)
    expected = _compute_expected_state()
    if rolled_back != expected:
        for key in expected:
            if rolled_back.get(key) != expected[key]:
                print(json.dumps({"test": "matches_expected", "passed": False,
                                  "message": f"Mismatch at '{key}': expected {expected[key]}, got {rolled_back.get(key)}"}))
                return
        print(json.dumps({"test": "matches_expected", "passed": False,
                          "message": "States differ (extra keys in rolled back state)"}))
        return
    print(json.dumps({"test": "matches_expected", "passed": True,
                      "message": "Rolled-back state matches expected state exactly"}))


def test_database_version_reverted():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "db_version", "passed": False, "message": "rolled_back_state.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = _compute_expected_state()
    expected_version = expected.get("database_version")
    if data.get("database_version") != expected_version:
        print(json.dumps({"test": "db_version", "passed": False,
                          "message": f"database_version should be '{expected_version}', got '{data.get('database_version')}'"}))
        return
    print(json.dumps({"test": "db_version", "passed": True,
                      "message": f"Database version reverted to {expected_version}"}))


def test_schema_reverted():
    path = os.path.join(CHALLENGE_DIR, "setup", "rolled_back_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "schema_reverted", "passed": False, "message": "rolled_back_state.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = _compute_expected_state()
    expected_columns = expected.get("schema", {}).get("users", {}).get("columns", [])
    columns = data.get("schema", {}).get("users", {}).get("columns", [])
    if columns != expected_columns:
        print(json.dumps({"test": "schema_reverted", "passed": False,
                          "message": f"users.columns should be {expected_columns}, got {columns}"}))
        return
    print(json.dumps({"test": "schema_reverted", "passed": True,
                      "message": "Schema reverted correctly"}))


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
    test_matches_expected()
    test_database_version_reverted()
    test_schema_reverted()
    test_rollback_log()
