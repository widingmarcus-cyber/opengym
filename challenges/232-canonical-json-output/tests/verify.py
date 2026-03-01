import json
import os
import subprocess
import sys
import hashlib

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_canonicalize():
    script = os.path.join(CHALLENGE_DIR, "setup", "canonicalize.py")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True,
        cwd=CHALLENGE_DIR
    )
    return result.returncode, result.stdout, result.stderr


def test_canonicalize_script_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "canonicalize.py")
    if not os.path.exists(path):
        print(json.dumps({"test": "canonicalize_script_exists", "passed": False, "message": "canonicalize.py not found in setup/"}))
        return False
    rc, stdout, stderr = _run_canonicalize()
    if rc != 0:
        print(json.dumps({"test": "canonicalize_script_exists", "passed": False, "message": f"canonicalize.py failed with exit code {rc}: {stderr.strip()}"}))
        return False
    output_path = os.path.join(CHALLENGE_DIR, "setup", "canonical.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "canonicalize_script_exists", "passed": False, "message": "canonicalize.py did not produce canonical.json"}))
        return False
    print(json.dumps({"test": "canonicalize_script_exists", "passed": True, "message": "canonicalize.py exists, runs, and produces canonical.json"}))
    return True


def test_valid_json_with_all_data():
    output_path = os.path.join(CHALLENGE_DIR, "setup", "canonical.json")
    input_path = os.path.join(CHALLENGE_DIR, "setup", "data.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "valid_json_with_all_data", "passed": False, "message": "canonical.json not found"}))
        return
    try:
        with open(output_path) as f:
            output_data = json.load(f)
        with open(input_path) as f:
            input_data = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "valid_json_with_all_data", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return
    # Compare data structures (ignoring key order)
    if json.dumps(output_data, sort_keys=True) == json.dumps(input_data, sort_keys=True):
        print(json.dumps({"test": "valid_json_with_all_data", "passed": True, "message": "canonical.json contains all data from data.json"}))
    else:
        print(json.dumps({"test": "valid_json_with_all_data", "passed": False, "message": "canonical.json data does not match data.json"}))


def test_sorted_keys():
    output_path = os.path.join(CHALLENGE_DIR, "setup", "canonical.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "sorted_keys", "passed": False, "message": "canonical.json not found"}))
        return
    with open(output_path) as f:
        content = f.read()
    data = json.loads(content)

    def check_sorted(obj, path=""):
        if isinstance(obj, dict):
            keys = list(obj.keys())
            if keys != sorted(keys):
                return False, f"Keys not sorted at {path or 'root'}: {keys}"
            for k, v in obj.items():
                ok, msg = check_sorted(v, f"{path}.{k}")
                if not ok:
                    return False, msg
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                ok, msg = check_sorted(item, f"{path}[{i}]")
                if not ok:
                    return False, msg
        return True, ""

    ok, msg = check_sorted(data)
    if ok:
        print(json.dumps({"test": "sorted_keys", "passed": True, "message": "All keys sorted lexicographically at all nesting levels"}))
    else:
        print(json.dumps({"test": "sorted_keys", "passed": False, "message": msg}))


def test_formatting_rules():
    output_path = os.path.join(CHALLENGE_DIR, "setup", "canonical.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "formatting_rules", "passed": False, "message": "canonical.json not found"}))
        return
    with open(output_path, "rb") as f:
        raw = f.read()
    content = raw.decode("utf-8")

    # Check trailing newline
    if not content.endswith("\n"):
        print(json.dumps({"test": "formatting_rules", "passed": False, "message": "File does not end with a trailing newline"}))
        return

    # Check no trailing whitespace on any line
    for i, line in enumerate(content.split("\n")[:-1], 1):  # Exclude final empty line after trailing \n
        if line != line.rstrip():
            print(json.dumps({"test": "formatting_rules", "passed": False, "message": f"Line {i} has trailing whitespace"}))
            return

    # Check 2-space indentation (spot check)
    lines = content.split("\n")
    found_indent = False
    for line in lines:
        stripped = line.lstrip()
        if stripped and line != stripped:
            indent = line[:len(line) - len(stripped)]
            if indent.replace("  ", "") != "":
                print(json.dumps({"test": "formatting_rules", "passed": False, "message": f"Non-2-space indentation found: '{indent}'"}))
                return
            found_indent = True

    if not found_indent:
        print(json.dumps({"test": "formatting_rules", "passed": False, "message": "No indentation found — file may not be pretty-printed"}))
        return

    print(json.dumps({"test": "formatting_rules", "passed": True, "message": "Formatting rules pass: 2-space indent, no trailing whitespace, trailing newline"}))


def test_byte_identical_across_runs():
    """Run canonicalize.py twice and verify byte-identical output."""
    _run_canonicalize()
    output_path = os.path.join(CHALLENGE_DIR, "setup", "canonical.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "byte_identical_across_runs", "passed": False, "message": "canonical.json not found after first run"}))
        return
    with open(output_path, "rb") as f:
        hash1 = hashlib.sha256(f.read()).hexdigest()

    _run_canonicalize()
    with open(output_path, "rb") as f:
        hash2 = hashlib.sha256(f.read()).hexdigest()

    if hash1 == hash2:
        print(json.dumps({"test": "byte_identical_across_runs", "passed": True, "message": f"Output is byte-identical across runs (SHA256: {hash1[:16]}...)"}))
    else:
        print(json.dumps({"test": "byte_identical_across_runs", "passed": False, "message": f"Output differs between runs: {hash1[:16]}... vs {hash2[:16]}..."}))


if __name__ == "__main__":
    test_canonicalize_script_exists()
    test_valid_json_with_all_data()
    test_sorted_keys()
    test_formatting_rules()
    test_byte_identical_across_runs()
