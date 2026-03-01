import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "setup/output.json not found"}))
        return False
    print(json.dumps({"test": "output_exists", "passed": True, "message": "output.json exists"}))
    return True


def test_all_records_present():
    path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_records_present", "passed": False, "message": "output.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) != 10:
        print(json.dumps({"test": "all_records_present", "passed": False,
                          "message": f"Expected 10 records, got {len(data) if isinstance(data, list) else 'non-list'}"}))
        return
    ids = sorted([r["id"] for r in data])
    if ids != list(range(1, 11)):
        print(json.dumps({"test": "all_records_present", "passed": False,
                          "message": f"Record IDs should be 1-10, got {ids}"}))
        return
    print(json.dumps({"test": "all_records_present", "passed": True, "message": "All 10 records present"}))


def test_records_processed_correctly():
    path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "records_processed", "passed": False, "message": "output.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    for rec in data:
        if rec.get("status") != "processed":
            print(json.dumps({"test": "records_processed", "passed": False,
                              "message": f"Record {rec.get('id')} missing status='processed'"}))
            return
        expected_result = f"{rec['value'].upper()}_x{rec['quantity']}"
        if rec.get("result") != expected_result:
            print(json.dumps({"test": "records_processed", "passed": False,
                              "message": f"Record {rec.get('id')} result should be '{expected_result}', got '{rec.get('result')}'"}))
            return
    print(json.dumps({"test": "records_processed", "passed": True, "message": "All records processed correctly"}))


def test_processor_bug_fixed():
    """Verify that the processor.py no longer crashes on zero-price items."""
    proc_path = os.path.join(CHALLENGE_DIR, "setup", "processor.py")
    if not os.path.exists(proc_path):
        print(json.dumps({"test": "processor_fixed", "passed": False, "message": "processor.py not found"}))
        return
    with open(proc_path) as f:
        code = f.read()
    # The original bug is a bare division: record['quantity'] / PRICE_LOOKUP[...]
    # A fix should handle zero prices — check that the original crashing line is changed
    if "record['quantity'] / PRICE_LOOKUP[record['value']]" in code:
        print(json.dumps({"test": "processor_fixed", "passed": False,
                          "message": "processor.py still contains the original crashing division line"}))
        return
    print(json.dumps({"test": "processor_fixed", "passed": True, "message": "Processor bug has been fixed"}))


def test_recovery_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "recovery_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "recovery_report", "passed": False, "message": "recovery_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    required_keys = ["crashed_on_record", "crash_reason", "records_recovered", "total_records"]
    for key in required_keys:
        if key not in report:
            print(json.dumps({"test": "recovery_report", "passed": False,
                              "message": f"recovery_report.json missing key '{key}'"}))
            return
    if report["crashed_on_record"] != 5:
        print(json.dumps({"test": "recovery_report", "passed": False,
                          "message": f"crashed_on_record should be 5, got {report['crashed_on_record']}"}))
        return
    if report["total_records"] != 10:
        print(json.dumps({"test": "recovery_report", "passed": False,
                          "message": f"total_records should be 10, got {report['total_records']}"}))
        return
    print(json.dumps({"test": "recovery_report", "passed": True, "message": "Recovery report is valid"}))


if __name__ == "__main__":
    test_output_exists()
    test_all_records_present()
    test_records_processed_correctly()
    test_processor_bug_fixed()
    test_recovery_report()
