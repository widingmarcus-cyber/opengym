import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_repaired_db_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "db_repaired.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "repaired_exists", "passed": False, "message": "db_repaired.json not found"}))
        return False
    print(json.dumps({"test": "repaired_exists", "passed": True, "message": "db_repaired.json exists"}))
    return True


def test_all_records_migrated():
    path = os.path.join(CHALLENGE_DIR, "setup", "db_repaired.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_migrated", "passed": False, "message": "db_repaired.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if len(data) != 20:
        print(json.dumps({"test": "all_migrated", "passed": False,
                          "message": f"Expected 20 records, got {len(data)}"}))
        return
    for rec in data:
        if rec.get("version") != 2:
            print(json.dumps({"test": "all_migrated", "passed": False,
                              "message": f"Record {rec.get('id')} has version={rec.get('version')}, expected 2"}))
            return
        expected_email = f"user_{rec['id']}@new.com"
        if rec.get("email") != expected_email:
            print(json.dumps({"test": "all_migrated", "passed": False,
                              "message": f"Record {rec['id']} email should be '{expected_email}', got '{rec.get('email')}'"}))
            return
    print(json.dumps({"test": "all_migrated", "passed": True, "message": "All 20 records fully migrated"}))


def test_roles_correct():
    path = os.path.join(CHALLENGE_DIR, "setup", "db_repaired.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "roles_correct", "passed": False, "message": "db_repaired.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    for rec in data:
        expected_role = "admin" if rec["id"] <= 5 else "member"
        if rec.get("role") != expected_role:
            print(json.dumps({"test": "roles_correct", "passed": False,
                              "message": f"Record {rec['id']} role should be '{expected_role}', got '{rec.get('role')}'"}))
            return
    print(json.dumps({"test": "roles_correct", "passed": True, "message": "All roles are correct"}))


def test_no_corrupted_fields():
    path = os.path.join(CHALLENGE_DIR, "setup", "db_repaired.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "no_corruption", "passed": False, "message": "db_repaired.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    required_fields = ["id", "name", "email", "role", "version"]
    for rec in data:
        for field in required_fields:
            if field not in rec or rec[field] is None:
                print(json.dumps({"test": "no_corruption", "passed": False,
                                  "message": f"Record {rec.get('id')} has missing/null field '{field}'"}))
                return
    print(json.dumps({"test": "no_corruption", "passed": True, "message": "No corrupted fields remain"}))


def test_damage_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "damage_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "damage_report", "passed": False, "message": "damage_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    if report.get("total_records") != 20:
        print(json.dumps({"test": "damage_report", "passed": False,
                          "message": f"total_records should be 20, got {report.get('total_records')}"}))
        return
    if report.get("all_repaired") is not True:
        print(json.dumps({"test": "damage_report", "passed": False,
                          "message": f"all_repaired should be true, got {report.get('all_repaired')}"}))
        return
    for key in ["clean_records", "corrupted_records", "untouched_records"]:
        if key not in report:
            print(json.dumps({"test": "damage_report", "passed": False,
                              "message": f"damage_report missing key '{key}'"}))
            return
    total = report["clean_records"] + report["corrupted_records"] + report["untouched_records"]
    if total != 20:
        print(json.dumps({"test": "damage_report", "passed": False,
                          "message": f"clean+corrupted+untouched should sum to 20, got {total}"}))
        return
    print(json.dumps({"test": "damage_report", "passed": True, "message": "Damage report is valid"}))


if __name__ == "__main__":
    test_repaired_db_exists()
    test_all_records_migrated()
    test_roles_correct()
    test_no_corrupted_fields()
    test_damage_report()
