import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE = os.path.join(CHALLENGE_DIR, "setup", "workspace")


def test_no_junk_files():
    junk_extensions = (".tmp", ".cache", ".partial")
    junk_files = [f for f in os.listdir(WORKSPACE) if any(f.endswith(ext) for ext in junk_extensions)]
    if junk_files:
        print(json.dumps({"test": "no_junk_files", "passed": False,
                          "message": f"Junk files still present: {junk_files}"}))
        return
    print(json.dumps({"test": "no_junk_files", "passed": True, "message": "No junk files in workspace"}))


def test_under_quota():
    quota_path = os.path.join(CHALLENGE_DIR, "setup", "quota.json")
    if not os.path.exists(quota_path):
        print(json.dumps({"test": "under_quota", "passed": False, "message": "quota.json not found"}))
        return
    with open(quota_path) as f:
        quota = json.load(f)
    total = sum(os.path.getsize(os.path.join(WORKSPACE, f)) for f in os.listdir(WORKSPACE))
    if total > quota["max_bytes"]:
        print(json.dumps({"test": "under_quota", "passed": False,
                          "message": f"Workspace is {total} bytes, exceeds quota of {quota['max_bytes']}"}))
        return
    print(json.dumps({"test": "under_quota", "passed": True, "message": f"Workspace {total} bytes is under quota"}))


def test_result_csv_exists():
    path = os.path.join(WORKSPACE, "result.csv")
    if not os.path.exists(path):
        print(json.dumps({"test": "result_csv", "passed": False, "message": "result.csv not found in workspace"}))
        return
    import csv
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if len(rows) != 20:
        print(json.dumps({"test": "result_csv", "passed": False,
                          "message": f"result.csv should have 20 rows, got {len(rows)}"}))
        return
    if "grade" not in rows[0]:
        print(json.dumps({"test": "result_csv", "passed": False, "message": "result.csv missing 'grade' column"}))
        return
    print(json.dumps({"test": "result_csv", "passed": True, "message": "result.csv is valid with 20 graded rows"}))


def test_data_csv_preserved():
    path = os.path.join(WORKSPACE, "data.csv")
    if not os.path.exists(path):
        print(json.dumps({"test": "data_preserved", "passed": False, "message": "data.csv was deleted!"}))
        return
    print(json.dumps({"test": "data_preserved", "passed": True, "message": "data.csv preserved"}))


def test_cleanup_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "cleanup_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "cleanup_report", "passed": False, "message": "cleanup_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    required = ["files_removed", "bytes_freed", "final_size_bytes", "quota_bytes"]
    for key in required:
        if key not in report:
            print(json.dumps({"test": "cleanup_report", "passed": False,
                              "message": f"cleanup_report.json missing key '{key}'"}))
            return
    if not isinstance(report["files_removed"], list) or len(report["files_removed"]) == 0:
        print(json.dumps({"test": "cleanup_report", "passed": False,
                          "message": "files_removed should be a non-empty list"}))
        return
    print(json.dumps({"test": "cleanup_report", "passed": True, "message": "Cleanup report is valid"}))


if __name__ == "__main__":
    test_no_junk_files()
    test_under_quota()
    test_result_csv_exists()
    test_data_csv_preserved()
    test_cleanup_report()
