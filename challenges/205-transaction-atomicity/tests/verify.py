import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(CHALLENGE_DIR, "setup", "config")


def test_all_configs_consistent():
    """All three config files must have version 2 (the new values)."""
    files = ["database.json", "cache.json", "api.json"]
    versions = []
    for fname in files:
        path = os.path.join(CONFIG_DIR, fname)
        if not os.path.exists(path):
            print(json.dumps({"test": "configs_consistent", "passed": False,
                              "message": f"{fname} not found"}))
            return
        try:
            with open(path) as f:
                data = json.load(f)
            versions.append(data.get("version"))
        except json.JSONDecodeError:
            print(json.dumps({"test": "configs_consistent", "passed": False,
                              "message": f"{fname} is corrupted (invalid JSON)"}))
            return
    if len(set(versions)) != 1:
        print(json.dumps({"test": "configs_consistent", "passed": False,
                          "message": f"Config versions are inconsistent: {dict(zip(files, versions))}"}))
        return
    if versions[0] != 2:
        print(json.dumps({"test": "configs_consistent", "passed": False,
                          "message": f"All configs should be version 2, got version {versions[0]}"}))
        return
    print(json.dumps({"test": "configs_consistent", "passed": True, "message": "All configs are consistent at version 2"}))


def test_database_config():
    path = os.path.join(CONFIG_DIR, "database.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "database_config", "passed": False, "message": "database.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "database_config", "passed": False, "message": "database.json is invalid JSON"}))
        return
    if data.get("host") != "db-new.example.com" or data.get("pool_size") != 20:
        print(json.dumps({"test": "database_config", "passed": False,
                          "message": f"database.json does not have intended new values"}))
        return
    print(json.dumps({"test": "database_config", "passed": True, "message": "database.json has correct new values"}))


def test_api_config():
    path = os.path.join(CONFIG_DIR, "api.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "api_config", "passed": False, "message": "api.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("base_url") != "https://api-new.example.com" or data.get("version") != 2:
        print(json.dumps({"test": "api_config", "passed": False,
                          "message": "api.json does not have intended new values"}))
        return
    print(json.dumps({"test": "api_config", "passed": True, "message": "api.json has correct new values"}))


def test_updater_uses_atomic_pattern():
    path = os.path.join(CHALLENGE_DIR, "setup", "config_updater.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "atomic_pattern", "passed": False, "message": "config_updater.py not found"}))
        return
    with open(path) as f:
        code = f.read()
    # Atomic write pattern involves temp files and rename/replace
    has_temp = "tmp" in code.lower() or "temp" in code.lower()
    has_rename = "rename" in code or "replace" in code or "shutil.move" in code
    if not (has_temp and has_rename):
        print(json.dumps({"test": "atomic_pattern", "passed": False,
                          "message": "config_updater.py does not use write-to-temp + rename pattern"}))
        return
    print(json.dumps({"test": "atomic_pattern", "passed": True, "message": "Updater uses atomic write pattern"}))


def test_transaction_log():
    path = os.path.join(CHALLENGE_DIR, "setup", "transaction_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "transaction_log", "passed": False, "message": "transaction_log.json not found"}))
        return
    with open(path) as f:
        log = json.load(f)
    if log.get("status") != "committed":
        print(json.dumps({"test": "transaction_log", "passed": False,
                          "message": f"status should be 'committed', got '{log.get('status')}'"}))
        return
    if log.get("atomic") is not True:
        print(json.dumps({"test": "transaction_log", "passed": False,
                          "message": "atomic should be true"}))
        return
    if not isinstance(log.get("files_updated"), list) or len(log.get("files_updated", [])) != 3:
        print(json.dumps({"test": "transaction_log", "passed": False,
                          "message": "files_updated should list 3 files"}))
        return
    print(json.dumps({"test": "transaction_log", "passed": True, "message": "Transaction log is valid"}))


if __name__ == "__main__":
    test_all_configs_consistent()
    test_database_config()
    test_api_config()
    test_updater_uses_atomic_pattern()
    test_transaction_log()
