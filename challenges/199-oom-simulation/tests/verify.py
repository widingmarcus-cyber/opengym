import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_summary_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "summary_exists", "passed": False, "message": "setup/summary.json not found"}))
        return False
    print(json.dumps({"test": "summary_exists", "passed": True, "message": "summary.json exists"}))
    return True


def test_summary_values():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "summary_values", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("total_records") != 5000:
        print(json.dumps({"test": "summary_values", "passed": False,
                          "message": f"total_records should be 5000, got {data.get('total_records')}"}))
        return
    if abs(data.get("avg_value", 0) - 500.86) > 0.01:
        print(json.dumps({"test": "summary_values", "passed": False,
                          "message": f"avg_value should be ~500.86, got {data.get('avg_value')}"}))
        return
    if data.get("max_value") != 999.91:
        print(json.dumps({"test": "summary_values", "passed": False,
                          "message": f"max_value should be 999.91, got {data.get('max_value')}"}))
        return
    if data.get("min_value") != 1.09:
        print(json.dumps({"test": "summary_values", "passed": False,
                          "message": f"min_value should be 1.09, got {data.get('min_value')}"}))
        return
    print(json.dumps({"test": "summary_values", "passed": True, "message": "Summary values are correct"}))


def test_processing_method():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "processing_method", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("processing_method") != "chunked":
        print(json.dumps({"test": "processing_method", "passed": False,
                          "message": f"processing_method must be 'chunked', got '{data.get('processing_method')}'"}))
        return
    print(json.dumps({"test": "processing_method", "passed": True, "message": "Processing method is chunked"}))


def test_aggregator_rewritten():
    path = os.path.join(CHALLENGE_DIR, "setup", "aggregator.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "aggregator_rewritten", "passed": False, "message": "aggregator.py not found"}))
        return
    with open(path) as f:
        code = f.read()
    # The original bulk approach has all_records.extend(data) and all_records.sort
    if "all_records.extend" in code and "all_records.sort" in code:
        print(json.dumps({"test": "aggregator_rewritten", "passed": False,
                          "message": "aggregator.py still uses bulk approach (extend + sort)"}))
        return
    if '"bulk"' in code and '"chunked"' not in code:
        print(json.dumps({"test": "aggregator_rewritten", "passed": False,
                          "message": "aggregator.py still uses 'bulk' processing_method"}))
        return
    print(json.dumps({"test": "aggregator_rewritten", "passed": True, "message": "Aggregator has been rewritten"}))


if __name__ == "__main__":
    test_summary_exists()
    test_summary_values()
    test_processing_method()
    test_aggregator_rewritten()
