import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_state_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "state_json", "passed": False, "message": "state.json not found"}))
        return
    with open(path) as f:
        state = json.load(f)
    if state.get("completed_stages") != [1, 2, 3]:
        print(json.dumps({"test": "state_json", "passed": False,
                          "message": f"completed_stages should be [1,2,3], got {state.get('completed_stages')}"}))
        return
    expected_data = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 225]
    if state.get("intermediate_data") != expected_data:
        print(json.dumps({"test": "state_json", "passed": False,
                          "message": f"intermediate_data after stage 3 is incorrect"}))
        return
    print(json.dumps({"test": "state_json", "passed": True, "message": "state.json is correct"}))


def test_checkpoint_json():
    path = os.path.join(CHALLENGE_DIR, "setup", "checkpoint.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "checkpoint_json", "passed": False, "message": "checkpoint.json not found"}))
        return
    with open(path) as f:
        cp = json.load(f)
    if cp.get("stage") != 3:
        print(json.dumps({"test": "checkpoint_json", "passed": False,
                          "message": f"checkpoint stage should be 3, got {cp.get('stage')}"}))
        return
    if cp.get("record_count") != 14:
        print(json.dumps({"test": "checkpoint_json", "passed": False,
                          "message": f"record_count should be 14, got {cp.get('record_count')}"}))
        return
    print(json.dumps({"test": "checkpoint_json", "passed": True, "message": "checkpoint.json is correct"}))


def test_final_report_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "final_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "final_report_exists", "passed": False, "message": "final_report.json not found"}))
        return False
    print(json.dumps({"test": "final_report_exists", "passed": True, "message": "final_report.json exists"}))
    return True


def test_final_report_values():
    path = os.path.join(CHALLENGE_DIR, "setup", "final_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "final_report_values", "passed": False, "message": "final_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    if report.get("pipeline_complete") is not True:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": "pipeline_complete should be true"}))
        return
    if report.get("recovered_from_crash") is not True:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": "recovered_from_crash should be true"}))
        return
    agg = report.get("aggregation", {})
    if agg.get("sum") != 875:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": f"aggregation sum should be 875, got {agg.get('sum')}"}))
        return
    if agg.get("count") != 14:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": f"aggregation count should be 14, got {agg.get('count')}"}))
        return
    if agg.get("mean") != 62.5:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": f"aggregation mean should be 62.5, got {agg.get('mean')}"}))
        return
    if agg.get("min") != 0:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": f"aggregation min should be 0, got {agg.get('min')}"}))
        return
    if agg.get("max") != 225:
        print(json.dumps({"test": "final_report_values", "passed": False,
                          "message": f"aggregation max should be 225, got {agg.get('max')}"}))
        return
    print(json.dumps({"test": "final_report_values", "passed": True, "message": "Final report values correct"}))


if __name__ == "__main__":
    test_state_json()
    test_checkpoint_json()
    test_final_report_exists()
    test_final_report_values()
