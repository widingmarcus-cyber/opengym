import json
import os
import subprocess
import sys
import hashlib

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_build():
    build_script = os.path.join(CHALLENGE_DIR, "setup", "build.py")
    result = subprocess.run(
        [sys.executable, build_script],
        capture_output=True, text=True,
        cwd=CHALLENGE_DIR
    )
    return result.returncode, result.stdout, result.stderr


def test_build_runs():
    returncode, stdout, stderr = _run_build()
    if returncode != 0:
        print(json.dumps({"test": "build_runs", "passed": False, "message": f"build.py exited with code {returncode}: {stderr.strip()}"}))
        return False
    output_path = os.path.join(CHALLENGE_DIR, "setup", "build_output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "build_runs", "passed": False, "message": "build.py did not produce build_output.json"}))
        return False
    print(json.dumps({"test": "build_runs", "passed": True, "message": "build.py runs successfully and produces build_output.json"}))
    return True


def test_output_has_required_fields():
    output_path = os.path.join(CHALLENGE_DIR, "setup", "build_output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "output_has_required_fields", "passed": False, "message": "build_output.json not found"}))
        return
    with open(output_path) as f:
        data = json.load(f)
    if "hash" not in data:
        print(json.dumps({"test": "output_has_required_fields", "passed": False, "message": "build_output.json missing 'hash' field"}))
        return
    if "files" not in data:
        print(json.dumps({"test": "output_has_required_fields", "passed": False, "message": "build_output.json missing 'files' field"}))
        return
    if "metadata" not in data:
        print(json.dumps({"test": "output_has_required_fields", "passed": False, "message": "build_output.json missing 'metadata' field"}))
        return
    print(json.dumps({"test": "output_has_required_fields", "passed": True, "message": "build_output.json has all required fields"}))


def test_all_source_files_included():
    output_path = os.path.join(CHALLENGE_DIR, "setup", "build_output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "all_source_files_included", "passed": False, "message": "build_output.json not found"}))
        return
    with open(output_path) as f:
        data = json.load(f)
    source_dir = os.path.join(CHALLENGE_DIR, "setup", "source")
    expected_files = sorted([f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))])
    actual_files = sorted(data.get("files", {}).keys())
    if expected_files != actual_files:
        print(json.dumps({"test": "all_source_files_included", "passed": False, "message": f"Expected files {expected_files}, got {actual_files}"}))
        return
    print(json.dumps({"test": "all_source_files_included", "passed": True, "message": f"All {len(expected_files)} source files included in build output"}))


def test_reproducible_hash():
    """Run build.py twice and verify identical output."""
    # First run
    rc1, _, stderr1 = _run_build()
    if rc1 != 0:
        print(json.dumps({"test": "reproducible_hash", "passed": False, "message": f"First build failed: {stderr1.strip()}"}))
        return
    output_path = os.path.join(CHALLENGE_DIR, "setup", "build_output.json")
    with open(output_path) as f:
        content1 = f.read()

    # Second run
    rc2, _, stderr2 = _run_build()
    if rc2 != 0:
        print(json.dumps({"test": "reproducible_hash", "passed": False, "message": f"Second build failed: {stderr2.strip()}"}))
        return
    with open(output_path) as f:
        content2 = f.read()

    if content1 == content2:
        hash1 = json.loads(content1).get("hash", "?")
        print(json.dumps({"test": "reproducible_hash", "passed": True, "message": f"Build is reproducible! Hash: {hash1}"}))
    else:
        hash1 = json.loads(content1).get("hash", "?")
        hash2 = json.loads(content2).get("hash", "?")
        print(json.dumps({"test": "reproducible_hash", "passed": False, "message": f"Build output differs between runs. Hash 1: {hash1}, Hash 2: {hash2}"}))


if __name__ == "__main__":
    test_build_runs()
    test_output_has_required_fields()
    test_all_source_files_included()
    test_reproducible_hash()
