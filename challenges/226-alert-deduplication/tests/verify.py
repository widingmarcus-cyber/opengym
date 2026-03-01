import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "deduplicated.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "deduplicated.json not found in setup/"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(json.dumps({"test": "output_exists", "passed": False, "message": "deduplicated.json must contain a JSON array"}))
            return False
        print(json.dumps({"test": "output_exists", "passed": True, "message": "deduplicated.json exists and is valid JSON array"}))
        return True
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "output_exists", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return False


def test_correct_group_count():
    path = os.path.join(CHALLENGE_DIR, "setup", "deduplicated.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "correct_group_count", "passed": False, "message": "deduplicated.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if len(data) == 5:
        print(json.dumps({"test": "correct_group_count", "passed": True, "message": "Correct: 20 alerts deduplicated into 5 groups"}))
    else:
        print(json.dumps({"test": "correct_group_count", "passed": False, "message": f"Expected 5 groups, got {len(data)}"}))


def test_alert_counts_per_group():
    path = os.path.join(CHALLENGE_DIR, "setup", "deduplicated.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "alert_counts_per_group", "passed": False, "message": "deduplicated.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected_counts = {
        "db-conn-fail-db-master-01": 8,
        "high-error-rate-api-server-03": 4,
        "disk-high-storage-node-02": 4,
        "cert-expiry-example-com": 2,
        "p99-latency-api-server-03": 2
    }
    for group in data:
        fp = group.get("fingerprint", "")
        expected = expected_counts.get(fp)
        if expected is None:
            print(json.dumps({"test": "alert_counts_per_group", "passed": False, "message": f"Unexpected fingerprint: '{fp}'"}))
            return
        actual = group.get("count", -1)
        if actual != expected:
            print(json.dumps({"test": "alert_counts_per_group", "passed": False, "message": f"Group '{fp}': expected count {expected}, got {actual}"}))
            return
        # Also check alert_ids length matches count
        ids_len = len(group.get("alert_ids", []))
        if ids_len != expected:
            print(json.dumps({"test": "alert_counts_per_group", "passed": False, "message": f"Group '{fp}': alert_ids length {ids_len} != count {expected}"}))
            return
    print(json.dumps({"test": "alert_counts_per_group", "passed": True, "message": "All group counts and alert_ids lengths are correct"}))


def test_severity_escalation():
    path = os.path.join(CHALLENGE_DIR, "setup", "deduplicated.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "severity_escalation", "passed": False, "message": "deduplicated.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    # disk-high-storage-node-02 has medium and high alerts, should show "high"
    for group in data:
        if group.get("fingerprint") == "disk-high-storage-node-02":
            if group.get("severity") != "high":
                print(json.dumps({"test": "severity_escalation", "passed": False, "message": f"disk-high group severity should be 'high' (escalated from medium), got '{group.get('severity')}'"}))
                return
            break
    else:
        print(json.dumps({"test": "severity_escalation", "passed": False, "message": "disk-high-storage-node-02 group not found"}))
        return
    print(json.dumps({"test": "severity_escalation", "passed": True, "message": "Severity correctly escalated to highest seen in group"}))


def test_sorted_by_first_seen():
    path = os.path.join(CHALLENGE_DIR, "setup", "deduplicated.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "sorted_by_first_seen", "passed": False, "message": "deduplicated.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    for i in range(1, len(data)):
        prev = data[i-1].get("first_seen", "")
        curr = data[i].get("first_seen", "")
        if curr < prev:
            print(json.dumps({"test": "sorted_by_first_seen", "passed": False, "message": f"Groups not sorted by first_seen: '{prev}' before '{curr}'"}))
            return
    print(json.dumps({"test": "sorted_by_first_seen", "passed": True, "message": "Groups correctly sorted by first_seen ascending"}))


if __name__ == "__main__":
    test_output_exists()
    test_correct_group_count()
    test_alert_counts_per_group()
    test_severity_escalation()
    test_sorted_by_first_seen()
