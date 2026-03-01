import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STAGE_NAMES = ["parse", "validate", "transform", "enrich", "dedupe", "sort", "partition", "aggregate", "format", "emit"]

def test_stage_outputs_exist():
    path = os.path.join(CHALLENGE_DIR, "setup", "stage_outputs.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "stage_outputs_exist", "passed": False, "message": "stage_outputs.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "stage_outputs_exist", "passed": True, "message": "stage_outputs.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "stage_outputs_exist", "passed": False, "message": "stage_outputs.json is not valid JSON"}))
        return None

def test_all_stages_present(data):
    if data is None:
        print(json.dumps({"test": "all_stages_present", "passed": False, "message": "No stage_outputs data to check"}))
        return
    missing = [s for s in STAGE_NAMES if s not in data]
    if missing:
        print(json.dumps({"test": "all_stages_present", "passed": False, "message": f"Missing stages: {missing}"}))
    else:
        print(json.dumps({"test": "all_stages_present", "passed": True, "message": "All 10 stages present in output"}))

def test_parse_stage(data):
    if data is None or "parse" not in data:
        print(json.dumps({"test": "parse_stage_correct", "passed": False, "message": "Parse stage output missing"}))
        return
    parsed = data["parse"]
    if not isinstance(parsed, list):
        print(json.dumps({"test": "parse_stage_correct", "passed": False, "message": "Parse stage output must be a list of records"}))
        return
    if len(parsed) != 13:
        print(json.dumps({"test": "parse_stage_correct", "passed": False, "message": f"Parse stage should produce 13 records from 13 raw strings, got {len(parsed)}"}))
        return
    first = parsed[0]
    if not isinstance(first, dict):
        print(json.dumps({"test": "parse_stage_correct", "passed": False, "message": "Parsed records must be dictionaries"}))
        return
    required_fields = {"id", "name", "country", "amount", "timestamp"}
    if not required_fields.issubset(set(first.keys())):
        print(json.dumps({"test": "parse_stage_correct", "passed": False, "message": f"Parsed record missing fields. Expected {required_fields}, got {set(first.keys())}"}))
        return
    print(json.dumps({"test": "parse_stage_correct", "passed": True, "message": "Parse stage correctly produced 13 structured records"}))

def test_validate_and_dedupe(data):
    if data is None:
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "No data to check"}))
        return
    if "validate" not in data:
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "Validate stage output missing"}))
        return
    valid = data["validate"]
    if not isinstance(valid, list):
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "Validate stage output must be a list"}))
        return
    # Record 10 (index 10, "10|missing_amount_field") should be invalid since it has insufficient fields
    valid_ids = [r.get("id") for r in valid if isinstance(r, dict)]
    # After validation, record with raw "10|missing_amount_field" should be removed (only 2 fields)
    if len(valid) > 12:
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": f"Validate stage should exclude invalid records. Got {len(valid)}, expected at most 12"}))
        return
    if "dedupe" not in data:
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "Dedupe stage output missing"}))
        return
    deduped = data["dedupe"]
    if not isinstance(deduped, list):
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "Dedupe stage output must be a list"}))
        return
    deduped_ids = [r.get("id") for r in deduped if isinstance(r, dict)]
    if len(deduped_ids) != len(set(deduped_ids)):
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": "Dedupe stage still contains duplicate IDs"}))
        return
    if len(deduped) != 10:
        print(json.dumps({"test": "validate_and_dedupe", "passed": False, "message": f"After validation and deduplication, expected 10 unique valid records, got {len(deduped)}"}))
        return
    print(json.dumps({"test": "validate_and_dedupe", "passed": True, "message": "Validate excluded invalid records and dedupe removed duplicates correctly (10 unique records)"}))

def test_pipeline_result_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "pipeline_result.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "pipeline_result_exists", "passed": False, "message": "pipeline_result.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "pipeline_result_exists", "passed": True, "message": "pipeline_result.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "pipeline_result_exists", "passed": False, "message": "pipeline_result.json is not valid JSON"}))
        return None

def test_aggregate_correctness(data):
    if data is None or "aggregate" not in data:
        print(json.dumps({"test": "aggregate_correctness", "passed": False, "message": "Aggregate stage output missing"}))
        return
    agg = data["aggregate"]
    if not isinstance(agg, dict):
        print(json.dumps({"test": "aggregate_correctness", "passed": False, "message": "Aggregate stage output must be a dict of partitions"}))
        return
    expected_regions = {"North America", "Europe", "Asia", "Oceania", "South America"}
    actual_regions = set(agg.keys())
    if not expected_regions.issubset(actual_regions):
        missing = expected_regions - actual_regions
        print(json.dumps({"test": "aggregate_correctness", "passed": False, "message": f"Missing region partitions: {list(missing)}"}))
        return
    for region, metrics in agg.items():
        if not isinstance(metrics, dict):
            print(json.dumps({"test": "aggregate_correctness", "passed": False, "message": f"Region '{region}' metrics must be a dict with count/sum/avg"}))
            return
        for metric in ["count", "sum", "avg"]:
            if metric not in metrics:
                print(json.dumps({"test": "aggregate_correctness", "passed": False, "message": f"Region '{region}' missing metric: {metric}"}))
                return
    print(json.dumps({"test": "aggregate_correctness", "passed": True, "message": "Aggregate stage has correct structure with all regions and metrics"}))

if __name__ == "__main__":
    data = test_stage_outputs_exist()
    test_all_stages_present(data)
    test_parse_stage(data)
    test_validate_and_dedupe(data)
    result = test_pipeline_result_exists()
    test_aggregate_correctness(data)
