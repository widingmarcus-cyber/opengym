import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LEVEL_ORDER = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}


def _load_source():
    path = os.path.join(CHALLENGE_DIR, "setup", "app_logs.json")
    with open(path) as f:
        return json.load(f)


def _count_at_level(entries, min_level):
    min_val = LEVEL_ORDER[min_level]
    return sum(1 for e in entries if LEVEL_ORDER.get(e["level"], -1) >= min_val)


def test_all_outputs_exist():
    files = ["filter_debug.json", "filter_info.json", "filter_warn.json", "filter_error.json"]
    missing = []
    for f in files:
        path = os.path.join(CHALLENGE_DIR, "setup", f)
        if not os.path.exists(path):
            missing.append(f)
    if missing:
        print(json.dumps({"test": "all_outputs_exist", "passed": False, "message": f"Missing output files: {missing}"}))
        return False
    # Validate each is a JSON array
    for f in files:
        path = os.path.join(CHALLENGE_DIR, "setup", f)
        try:
            with open(path) as fh:
                data = json.load(fh)
            if not isinstance(data, list):
                print(json.dumps({"test": "all_outputs_exist", "passed": False, "message": f"{f} is not a JSON array"}))
                return False
        except json.JSONDecodeError as e:
            print(json.dumps({"test": "all_outputs_exist", "passed": False, "message": f"{f} has invalid JSON: {str(e)}"}))
            return False
    print(json.dumps({"test": "all_outputs_exist", "passed": True, "message": "All 4 filter output files exist and are valid JSON arrays"}))
    return True


def test_debug_filter_count():
    source = _load_source()
    path = os.path.join(CHALLENGE_DIR, "setup", "filter_debug.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "debug_filter_count", "passed": False, "message": "filter_debug.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = _count_at_level(source, "DEBUG")  # All entries = 20
    if len(data) == expected:
        print(json.dumps({"test": "debug_filter_count", "passed": True, "message": f"filter_debug.json has correct count: {expected}"}))
    else:
        print(json.dumps({"test": "debug_filter_count", "passed": False, "message": f"filter_debug.json: expected {expected} entries, got {len(data)}"}))


def test_warn_filter_count():
    source = _load_source()
    path = os.path.join(CHALLENGE_DIR, "setup", "filter_warn.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "warn_filter_count", "passed": False, "message": "filter_warn.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = _count_at_level(source, "WARN")  # WARN + ERROR = 4 + 3 = 7
    if len(data) == expected:
        print(json.dumps({"test": "warn_filter_count", "passed": True, "message": f"filter_warn.json has correct count: {expected}"}))
    else:
        print(json.dumps({"test": "warn_filter_count", "passed": False, "message": f"filter_warn.json: expected {expected} entries, got {len(data)}"}))


def test_error_filter_count():
    source = _load_source()
    path = os.path.join(CHALLENGE_DIR, "setup", "filter_error.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "error_filter_count", "passed": False, "message": "filter_error.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = _count_at_level(source, "ERROR")  # ERROR only = 3
    if len(data) == expected:
        print(json.dumps({"test": "error_filter_count", "passed": True, "message": f"filter_error.json has correct count: {expected}"}))
    else:
        print(json.dumps({"test": "error_filter_count", "passed": False, "message": f"filter_error.json: expected {expected} entries, got {len(data)}"}))


def test_entries_unmodified():
    source = _load_source()
    path = os.path.join(CHALLENGE_DIR, "setup", "filter_info.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "entries_unmodified", "passed": False, "message": "filter_info.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    # Each entry in filter_info should match an original entry exactly
    source_set = [json.dumps(e, sort_keys=True) for e in source if LEVEL_ORDER.get(e["level"], -1) >= LEVEL_ORDER["INFO"]]
    data_set = [json.dumps(e, sort_keys=True) for e in data]
    if source_set == data_set:
        print(json.dumps({"test": "entries_unmodified", "passed": True, "message": "Entries in filter_info.json match source exactly (fields and order preserved)"}))
    else:
        print(json.dumps({"test": "entries_unmodified", "passed": False, "message": "Entries in filter_info.json do not match expected filtered source entries (check field preservation and order)"}))


if __name__ == "__main__":
    test_all_outputs_exist()
    test_debug_filter_count()
    test_warn_filter_count()
    test_error_filter_count()
    test_entries_unmodified()
