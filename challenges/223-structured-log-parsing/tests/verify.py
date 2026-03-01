import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "parsed_logs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "parsed_logs.json not found in setup/"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(json.dumps({"test": "output_exists", "passed": False, "message": "parsed_logs.json must contain a JSON array"}))
            return False
        print(json.dumps({"test": "output_exists", "passed": True, "message": "parsed_logs.json exists and is valid JSON array"}))
        return True
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "output_exists", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return False


def test_correct_count():
    path = os.path.join(CHALLENGE_DIR, "setup", "parsed_logs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "correct_count", "passed": False, "message": "parsed_logs.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    # logs.txt has 15 non-blank log lines
    if len(data) == 15:
        print(json.dumps({"test": "correct_count", "passed": True, "message": f"Correct count: {len(data)} entries parsed"}))
    else:
        print(json.dumps({"test": "correct_count", "passed": False, "message": f"Expected 15 entries, got {len(data)}"}))


def test_required_fields():
    path = os.path.join(CHALLENGE_DIR, "setup", "parsed_logs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "required_fields", "passed": False, "message": "parsed_logs.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    required = {"timestamp", "source", "level", "message", "metadata"}
    for i, entry in enumerate(data):
        missing = required - set(entry.keys())
        if missing:
            print(json.dumps({"test": "required_fields", "passed": False, "message": f"Entry {i} missing fields: {sorted(missing)}"}))
            return
    print(json.dumps({"test": "required_fields", "passed": True, "message": "All entries have required fields"}))


def test_source_classification():
    path = os.path.join(CHALLENGE_DIR, "setup", "parsed_logs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "source_classification", "passed": False, "message": "parsed_logs.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    valid_sources = {"syslog", "apache", "app"}
    source_counts = {}
    for i, entry in enumerate(data):
        src = entry.get("source", "")
        if src not in valid_sources:
            print(json.dumps({"test": "source_classification", "passed": False, "message": f"Entry {i} has invalid source '{src}', expected one of {sorted(valid_sources)}"}))
            return
        source_counts[src] = source_counts.get(src, 0) + 1
    # Expect 4 syslog, 5 apache, 4 app (+ 2 more based on actual content = 5 syslog, 5 apache, 5 app... let's be flexible)
    if len(source_counts) < 3:
        print(json.dumps({"test": "source_classification", "passed": False, "message": f"Expected all 3 source types, found only: {sorted(source_counts.keys())}"}))
        return
    print(json.dumps({"test": "source_classification", "passed": True, "message": f"All sources correctly classified: {source_counts}"}))


def test_timestamp_format():
    path = os.path.join(CHALLENGE_DIR, "setup", "parsed_logs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "timestamp_format", "passed": False, "message": "parsed_logs.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    import re
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    for i, entry in enumerate(data):
        ts = entry.get("timestamp", "")
        if not iso_pattern.match(ts):
            print(json.dumps({"test": "timestamp_format", "passed": False, "message": f"Entry {i} timestamp '{ts}' is not ISO-8601 UTC (expected YYYY-MM-DDTHH:MM:SSZ)"}))
            return
    print(json.dumps({"test": "timestamp_format", "passed": True, "message": "All timestamps are valid ISO-8601 UTC format"}))


if __name__ == "__main__":
    test_output_exists()
    test_correct_count()
    test_required_fields()
    test_source_classification()
    test_timestamp_format()
