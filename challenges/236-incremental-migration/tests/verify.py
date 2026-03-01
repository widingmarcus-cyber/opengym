import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_batch_1_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "batch_1.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "batch_1_exists", "passed": False, "message": "batch_1.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "batch_1_exists", "passed": True, "message": "batch_1.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "batch_1_exists", "passed": False, "message": "batch_1.json is not valid JSON"}))
        return None

def test_batch_1_records(data):
    if data is None:
        print(json.dumps({"test": "batch_1_records", "passed": False, "message": "No batch_1 data to check"}))
        return
    records = data.get("records", [])
    if len(records) != 10:
        print(json.dumps({"test": "batch_1_records", "passed": False, "message": f"batch_1 should have 10 records, got {len(records)}"}))
        return
    ids = [r.get("id") for r in records]
    expected_ids = list(range(1, 11))
    if sorted(ids) != expected_ids:
        print(json.dumps({"test": "batch_1_records", "passed": False, "message": f"batch_1 should have record IDs 1-10, got {sorted(ids)}"}))
        return
    # Check field mapping was applied (legacy field names should not be present)
    first = records[0]
    legacy_fields = {"record_id", "cust_name", "cust_email", "purchase_amt", "purchase_date", "active_flag"}
    found_legacy = legacy_fields.intersection(set(first.keys()))
    if found_legacy:
        print(json.dumps({"test": "batch_1_records", "passed": False, "message": f"batch_1 records still contain legacy fields: {list(found_legacy)}"}))
        return
    print(json.dumps({"test": "batch_1_records", "passed": True, "message": "batch_1 has 10 records with correct IDs and field mappings applied"}))

def test_batch_2_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "batch_2.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "batch_2_exists", "passed": False, "message": "batch_2.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "batch_2_exists", "passed": True, "message": "batch_2.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "batch_2_exists", "passed": False, "message": "batch_2.json is not valid JSON"}))
        return None

def test_schema_v2_applied(batch1, batch2):
    if batch1 is None and batch2 is None:
        print(json.dumps({"test": "schema_v2_applied", "passed": False, "message": "No batch data to check"}))
        return
    errors = []
    for name, data in [("batch_1", batch1), ("batch_2", batch2)]:
        if data is None:
            errors.append(f"{name} is missing")
            continue
        if data.get("schema_version") != "v2":
            errors.append(f"{name} schema_version should be 'v2', got '{data.get('schema_version')}'")
        for r in data.get("records", []):
            # v2: customer_name renamed to full_name, category removed, new fields added
            if "customer_name" in r:
                errors.append(f"{name} record {r.get('id')}: 'customer_name' should be renamed to 'full_name'")
                break
            if "full_name" not in r:
                errors.append(f"{name} record {r.get('id')}: missing 'full_name' field (v2 rename)")
                break
            if "category" in r:
                errors.append(f"{name} record {r.get('id')}: 'category' should be removed in v2")
                break
            if "migrated_at" not in r:
                errors.append(f"{name} record {r.get('id')}: missing 'migrated_at' field (v2 new field)")
                break
            if "source_system" not in r:
                errors.append(f"{name} record {r.get('id')}: missing 'source_system' field (v2 new field)")
                break
    if errors:
        print(json.dumps({"test": "schema_v2_applied", "passed": False, "message": "; ".join(errors)}))
    else:
        print(json.dumps({"test": "schema_v2_applied", "passed": True, "message": "Schema v2 changes correctly applied to both batches"}))

def test_reconciliation():
    path = os.path.join(CHALLENGE_DIR, "setup", "reconciliation.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "reconciliation", "passed": False, "message": "reconciliation.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "reconciliation", "passed": False, "message": "reconciliation.json is not valid JSON"}))
        return
    if data.get("total_source_records") != 20:
        print(json.dumps({"test": "reconciliation", "passed": False, "message": f"total_source_records should be 20, got {data.get('total_source_records')}"}))
        return
    if data.get("total_migrated_records") != 20:
        print(json.dumps({"test": "reconciliation", "passed": False, "message": f"total_migrated_records should be 20, got {data.get('total_migrated_records')}"}))
        return
    if data.get("all_records_migrated") is not True:
        print(json.dumps({"test": "reconciliation", "passed": False, "message": "all_records_migrated should be true"}))
        return
    missing = data.get("missing_records", [])
    if len(missing) != 0:
        print(json.dumps({"test": "reconciliation", "passed": False, "message": f"missing_records should be empty, got {missing}"}))
        return
    if data.get("status") != "complete":
        print(json.dumps({"test": "reconciliation", "passed": False, "message": f"status should be 'complete', got '{data.get('status')}'"}))
        return
    print(json.dumps({"test": "reconciliation", "passed": True, "message": "Reconciliation report is correct: all 20 records migrated"}))

def test_type_conversions():
    # Check that amount is float and is_active is boolean in migrated records
    batch1_path = os.path.join(CHALLENGE_DIR, "setup", "batch_1.json")
    if not os.path.exists(batch1_path):
        print(json.dumps({"test": "type_conversions", "passed": False, "message": "batch_1.json not found"}))
        return
    with open(batch1_path) as f:
        data = json.load(f)
    records = data.get("records", [])
    if not records:
        print(json.dumps({"test": "type_conversions", "passed": False, "message": "No records in batch_1"}))
        return
    for r in records:
        amt = r.get("amount")
        active = r.get("is_active")
        if not isinstance(amt, (int, float)):
            print(json.dumps({"test": "type_conversions", "passed": False, "message": f"Record {r.get('id')}: 'amount' should be a number, got {type(amt).__name__}"}))
            return
        if not isinstance(active, bool):
            print(json.dumps({"test": "type_conversions", "passed": False, "message": f"Record {r.get('id')}: 'is_active' should be boolean, got {type(active).__name__}"}))
            return
    print(json.dumps({"test": "type_conversions", "passed": True, "message": "Type conversions applied correctly: amount is float, is_active is boolean"}))

if __name__ == "__main__":
    batch1 = test_batch_1_exists()
    test_batch_1_records(batch1)
    batch2 = test_batch_2_exists()
    test_schema_v2_applied(batch1, batch2)
    test_reconciliation()
    test_type_conversions()
