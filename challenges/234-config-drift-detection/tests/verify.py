import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Known drifts between baseline and current:
# web-01: memory_gb 16->8, firewall.https_enabled true->false, firewall.custom_ports [8080]->[8080,9090]
# web-02: os ubuntu-22.04->ubuntu-20.04, services [nginx,node]->[nginx], env production->staging
# db-01: firewall.ssh_enabled true->false
# cache-01: cpu_cores 4->2, services [redis]->[redis,memcached], firewall.custom_ports [6379]->[6379,11211]
# worker-01: auto_update true->false
EXPECTED_DRIFT_COUNT = 10

def test_baseline_snapshot():
    path = os.path.join(CHALLENGE_DIR, "setup", "baseline_snapshot.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "baseline_snapshot", "passed": False, "message": "baseline_snapshot.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "baseline_snapshot", "passed": False, "message": "baseline_snapshot.json is not valid JSON"}))
        return
    if "server_count" not in data or data["server_count"] != 5:
        print(json.dumps({"test": "baseline_snapshot", "passed": False, "message": "baseline_snapshot.json must have server_count = 5"}))
        return
    if "timestamp" not in data:
        print(json.dumps({"test": "baseline_snapshot", "passed": False, "message": "baseline_snapshot.json must have a timestamp field"}))
        return
    if "servers" not in data or not isinstance(data["servers"], dict) or len(data["servers"]) != 5:
        print(json.dumps({"test": "baseline_snapshot", "passed": False, "message": "baseline_snapshot.json must have servers dict with 5 entries"}))
        return
    print(json.dumps({"test": "baseline_snapshot", "passed": True, "message": "Baseline snapshot is correct"}))

def test_drift_report_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "drift_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "drift_report_exists", "passed": False, "message": "drift_report.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "drift_report_exists", "passed": True, "message": "drift_report.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "drift_report_exists", "passed": False, "message": "drift_report.json is not valid JSON"}))
        return None

def test_drift_count(data):
    if data is None:
        print(json.dumps({"test": "drift_count", "passed": False, "message": "No drift report to check"}))
        return
    total = data.get("total_drifts", 0)
    drifts = data.get("drifts", [])
    if total < EXPECTED_DRIFT_COUNT:
        print(json.dumps({"test": "drift_count", "passed": False, "message": f"Expected at least {EXPECTED_DRIFT_COUNT} drifts, got {total}"}))
        return
    if len(drifts) != total:
        print(json.dumps({"test": "drift_count", "passed": False, "message": f"total_drifts ({total}) does not match number of drift entries ({len(drifts)})"}))
        return
    print(json.dumps({"test": "drift_count", "passed": True, "message": f"Drift count is correct: {total} drifts detected"}))

def test_drift_detail(data):
    if data is None or "drifts" not in data:
        print(json.dumps({"test": "drift_detail", "passed": False, "message": "No drifts to check"}))
        return
    drifts = data["drifts"]
    servers_with_drifts = set()
    for d in drifts:
        if not all(k in d for k in ["server", "field", "baseline_value", "current_value"]):
            print(json.dumps({"test": "drift_detail", "passed": False, "message": "Each drift must have server, field, baseline_value, current_value"}))
            return
        servers_with_drifts.add(d["server"])
    expected_servers = {"web-01", "web-02", "db-01", "cache-01", "worker-01"}
    missing = expected_servers - servers_with_drifts
    if missing:
        print(json.dumps({"test": "drift_detail", "passed": False, "message": f"Missing drift detection for servers: {list(missing)}"}))
        return
    print(json.dumps({"test": "drift_detail", "passed": True, "message": "Drifts detected across all 5 servers correctly"}))

def test_remediation_plan():
    path = os.path.join(CHALLENGE_DIR, "setup", "remediation_plan.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "remediation_plan", "passed": False, "message": "remediation_plan.json not found"}))
        return
    try:
        with open(path) as f:
            plan = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "remediation_plan", "passed": False, "message": "remediation_plan.json is not valid JSON"}))
        return
    if "total_remediations" not in plan or "remediations" not in plan:
        print(json.dumps({"test": "remediation_plan", "passed": False, "message": "remediation_plan.json must have total_remediations and remediations"}))
        return
    drift_path = os.path.join(CHALLENGE_DIR, "setup", "drift_report.json")
    if os.path.exists(drift_path):
        with open(drift_path) as f:
            drift_data = json.load(f)
        if plan["total_remediations"] != drift_data.get("total_drifts", 0):
            print(json.dumps({"test": "remediation_plan", "passed": False, "message": f"total_remediations ({plan['total_remediations']}) must equal total_drifts ({drift_data.get('total_drifts', 0)})"}))
            return
    remediations = plan["remediations"]
    for r in remediations:
        if not all(k in r for k in ["server", "field", "action", "target_value"]):
            print(json.dumps({"test": "remediation_plan", "passed": False, "message": "Each remediation must have server, field, action, target_value"}))
            return
    print(json.dumps({"test": "remediation_plan", "passed": True, "message": f"Remediation plan is complete with {plan['total_remediations']} actions"}))

def test_remediation_targets_baseline():
    plan_path = os.path.join(CHALLENGE_DIR, "setup", "remediation_plan.json")
    baseline_path = os.path.join(CHALLENGE_DIR, "setup", "baseline_config.json")
    if not os.path.exists(plan_path) or not os.path.exists(baseline_path):
        print(json.dumps({"test": "remediation_targets_baseline", "passed": False, "message": "remediation_plan.json or baseline_config.json not found"}))
        return
    with open(plan_path) as f:
        plan = json.load(f)
    with open(baseline_path) as f:
        baseline = json.load(f)
    for r in plan.get("remediations", []):
        server = r.get("server", "")
        field = r.get("field", "")
        target = r.get("target_value")
        if server not in baseline.get("servers", {}):
            print(json.dumps({"test": "remediation_targets_baseline", "passed": False, "message": f"Unknown server in remediation: {server}"}))
            return
        server_config = baseline["servers"][server]
        parts = field.split(".")
        value = server_config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                print(json.dumps({"test": "remediation_targets_baseline", "passed": False, "message": f"Cannot resolve field path '{field}' in baseline for server '{server}'"}))
                return
        if value != target:
            print(json.dumps({"test": "remediation_targets_baseline", "passed": False, "message": f"Remediation target for {server}.{field} should be {value}, got {target}"}))
            return
    print(json.dumps({"test": "remediation_targets_baseline", "passed": True, "message": "All remediation target values match baseline"}))

if __name__ == "__main__":
    test_baseline_snapshot()
    drift_data = test_drift_report_exists()
    test_drift_count(drift_data)
    test_drift_detail(drift_data)
    test_remediation_plan()
    test_remediation_targets_baseline()
