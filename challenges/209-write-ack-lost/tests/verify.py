import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_verified_store_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "data_store_verified.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "verified_store_exists", "passed": False,
                          "message": "data_store_verified.json not found"}))
        return
    print(json.dumps({"test": "verified_store_exists", "passed": True,
                      "message": "data_store_verified.json exists"}))


def test_all_records_present():
    path = os.path.join(CHALLENGE_DIR, "setup", "data_store_verified.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_records", "passed": False, "message": "data_store_verified.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if len(data) != 12:
        print(json.dumps({"test": "all_records", "passed": False,
                          "message": f"Should have 12 records, got {len(data)}"}))
        return
    ids = sorted([r["record_id"] for r in data])
    expected = [f"R{i:03d}" for i in range(1, 13)]
    if ids != expected:
        print(json.dumps({"test": "all_records", "passed": False,
                          "message": f"Record IDs should be R001-R012, got {ids}"}))
        return
    print(json.dumps({"test": "all_records", "passed": True, "message": "All 12 records present"}))


def test_data_integrity():
    path = os.path.join(CHALLENGE_DIR, "setup", "data_store_verified.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "data_integrity", "passed": False, "message": "data_store_verified.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    for rec in data:
        rid = rec["record_id"]
        num = int(rid[1:])
        expected_data = f"payload_{num}"
        expected_chk = f"chk_{num}"
        if rec.get("data") != expected_data or rec.get("checksum") != expected_chk:
            print(json.dumps({"test": "data_integrity", "passed": False,
                              "message": f"Record {rid} has incorrect data or checksum"}))
            return
    print(json.dumps({"test": "data_integrity", "passed": True, "message": "All record data/checksums correct"}))


def test_reconciliation_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "reconciliation_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "reconciliation_report", "passed": False,
                          "message": "reconciliation_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    if report.get("total_writes") != 12:
        print(json.dumps({"test": "reconciliation_report", "passed": False,
                          "message": f"total_writes should be 12, got {report.get('total_writes')}"}))
        return
    if report.get("all_verified") is not True:
        print(json.dumps({"test": "reconciliation_report", "passed": False,
                          "message": "all_verified should be true"}))
        return
    lost = sorted(report.get("lost_acks", []))
    if lost != ["R006", "R009"]:
        print(json.dumps({"test": "reconciliation_report", "passed": False,
                          "message": f"lost_acks should be ['R006','R009'], got {lost}"}))
        return
    missing = sorted(report.get("missing_writes", []))
    if missing != ["R007", "R010", "R011", "R012"]:
        print(json.dumps({"test": "reconciliation_report", "passed": False,
                          "message": f"missing_writes should be ['R007','R010','R011','R012'], got {missing}"}))
        return
    print(json.dumps({"test": "reconciliation_report", "passed": True,
                      "message": "Reconciliation report is correct"}))


if __name__ == "__main__":
    test_verified_store_exists()
    test_all_records_present()
    test_data_integrity()
    test_reconciliation_report()
