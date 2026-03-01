import json
import os
import ast

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_analysis_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "analysis.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "analysis_exists", "passed": False, "message": "setup/analysis.json not found"}))
        return False
    print(json.dumps({"test": "analysis_exists", "passed": True, "message": "analysis.json exists"}))
    return True


def test_analysis_values():
    path = os.path.join(CHALLENGE_DIR, "setup", "analysis.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "analysis_values", "passed": False, "message": "analysis.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("total_lines") != 968:
        print(json.dumps({"test": "analysis_values", "passed": False,
                          "message": f"total_lines should be 968, got {data.get('total_lines')}"}))
        return
    if data.get("error_count") != 138:
        print(json.dumps({"test": "analysis_values", "passed": False,
                          "message": f"error_count should be 138, got {data.get('error_count')}"}))
        return
    if data.get("warning_count") != 127:
        print(json.dumps({"test": "analysis_values", "passed": False,
                          "message": f"warning_count should be 127, got {data.get('warning_count')}"}))
        return
    if data.get("files_processed") != 50:
        print(json.dumps({"test": "analysis_values", "passed": False,
                          "message": f"files_processed should be 50, got {data.get('files_processed')}"}))
        return
    print(json.dumps({"test": "analysis_values", "passed": True, "message": "Analysis values are correct"}))


def test_max_concurrent_fds():
    path = os.path.join(CHALLENGE_DIR, "setup", "analysis.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "max_concurrent_fds", "passed": False, "message": "analysis.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    max_fds = data.get("max_concurrent_fds", 999)
    if max_fds > 5:
        print(json.dumps({"test": "max_concurrent_fds", "passed": False,
                          "message": f"max_concurrent_fds should be <= 5, got {max_fds}"}))
        return
    print(json.dumps({"test": "max_concurrent_fds", "passed": True,
                      "message": f"max_concurrent_fds is {max_fds}"}))


def test_analyzer_rewritten():
    path = os.path.join(CHALLENGE_DIR, "setup", "analyzer.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "analyzer_rewritten", "passed": False, "message": "analyzer.py not found"}))
        return
    with open(path) as f:
        code = f.read()
    # The original leaky pattern: open() without close/with, appending to open_handles
    if "open_handles" in code and "open_handles.append" in code:
        print(json.dumps({"test": "analyzer_rewritten", "passed": False,
                          "message": "analyzer.py still accumulates open file handles in a list"}))
        return
    print(json.dumps({"test": "analyzer_rewritten", "passed": True,
                      "message": "Analyzer no longer accumulates file handles"}))


if __name__ == "__main__":
    test_analysis_exists()
    test_analysis_values()
    test_max_concurrent_fds()
    test_analyzer_rewritten()
