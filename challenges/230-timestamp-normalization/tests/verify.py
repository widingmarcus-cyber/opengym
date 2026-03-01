import json
import os
import re

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Expected normalized timestamps (all UTC)
EXPECTED = {
    "evt-001": "2025-01-05T14:00:00Z",
    "evt-002": "2025-01-05T14:00:00Z",
    "evt-003": "2025-01-05T14:00:00Z",
    "evt-004": "2025-01-05T15:30:00Z",
    "evt-005": "2025-01-05T15:50:00Z",
    "evt-006": "2025-01-05T16:45:00Z",
    "evt-007": "2025-01-05T15:00:00Z",
    "evt-008": "2025-01-05T14:00:00Z",
    "evt-009": "2025-01-05T16:30:00Z",
    "evt-010": "2025-01-05T19:00:00Z",
    "evt-011": "2025-01-05T20:00:00Z",
    "evt-012": "2025-01-05T15:45:00Z",
}


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "normalized.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "normalized.json not found in setup/"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(json.dumps({"test": "output_exists", "passed": False, "message": "normalized.json must contain a JSON array"}))
            return False
        print(json.dumps({"test": "output_exists", "passed": True, "message": "normalized.json exists and is valid JSON array"}))
        return True
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "output_exists", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return False


def test_correct_count():
    path = os.path.join(CHALLENGE_DIR, "setup", "normalized.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "correct_count", "passed": False, "message": "normalized.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if len(data) == 12:
        print(json.dumps({"test": "correct_count", "passed": True, "message": "All 12 events present"}))
    else:
        print(json.dumps({"test": "correct_count", "passed": False, "message": f"Expected 12 events, got {len(data)}"}))


def test_all_iso8601_utc():
    path = os.path.join(CHALLENGE_DIR, "setup", "normalized.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_iso8601_utc", "passed": False, "message": "normalized.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    for i, event in enumerate(data):
        ts = event.get("timestamp", "")
        if not isinstance(ts, str) or not iso_pattern.match(ts):
            print(json.dumps({"test": "all_iso8601_utc", "passed": False, "message": f"Event {i} ('{event.get('event_id', '?')}') timestamp '{ts}' is not ISO-8601 UTC format"}))
            return
    print(json.dumps({"test": "all_iso8601_utc", "passed": True, "message": "All timestamps are valid ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)"}))


def test_timestamps_correct():
    path = os.path.join(CHALLENGE_DIR, "setup", "normalized.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "timestamps_correct", "passed": False, "message": "normalized.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    errors = []
    for event in data:
        eid = event.get("event_id", "?")
        actual = event.get("timestamp", "")
        expected = EXPECTED.get(eid)
        if expected is None:
            errors.append(f"Unknown event_id: {eid}")
            continue
        if actual != expected:
            errors.append(f"{eid}: expected '{expected}', got '{actual}'")
    if errors:
        print(json.dumps({"test": "timestamps_correct", "passed": False, "message": f"Incorrect timestamps: {'; '.join(errors[:3])}"}))
    else:
        print(json.dumps({"test": "timestamps_correct", "passed": True, "message": "All 12 timestamps correctly normalized to UTC"}))


def test_other_fields_preserved():
    path = os.path.join(CHALLENGE_DIR, "setup", "normalized.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "other_fields_preserved", "passed": False, "message": "normalized.json not found"}))
        return
    source_path = os.path.join(CHALLENGE_DIR, "setup", "events.json")
    with open(source_path) as f:
        source = json.load(f)
    with open(path) as f:
        data = json.load(f)
    source_by_id = {e["event_id"]: e for e in source}
    for event in data:
        eid = event.get("event_id", "?")
        orig = source_by_id.get(eid)
        if orig is None:
            print(json.dumps({"test": "other_fields_preserved", "passed": False, "message": f"Unknown event_id: {eid}"}))
            return
        for key in orig:
            if key == "timestamp":
                continue
            if key not in event or event[key] != orig[key]:
                print(json.dumps({"test": "other_fields_preserved", "passed": False, "message": f"Event '{eid}' field '{key}' was modified or missing"}))
                return
    print(json.dumps({"test": "other_fields_preserved", "passed": True, "message": "All non-timestamp fields preserved unchanged"}))


if __name__ == "__main__":
    test_output_exists()
    test_correct_count()
    test_all_iso8601_utc()
    test_timestamps_correct()
    test_other_fields_preserved()
