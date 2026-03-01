import json
import os
import subprocess
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _clean_outputs():
    """Remove output files so each test starts fresh."""
    for fname in ["output.json", "state.json"]:
        path = os.path.join(CHALLENGE_DIR, "setup", fname)
        if os.path.exists(path):
            os.remove(path)


def _run_process():
    script = os.path.join(CHALLENGE_DIR, "setup", "process.py")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True,
        cwd=CHALLENGE_DIR
    )
    return result.returncode, result.stdout, result.stderr


def test_runs_successfully():
    _clean_outputs()
    rc, stdout, stderr = _run_process()
    if rc != 0:
        print(json.dumps({"test": "runs_successfully", "passed": False, "message": f"process.py exited with code {rc}: {stderr.strip()}"}))
        return False
    output_path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "runs_successfully", "passed": False, "message": "process.py did not produce output.json"}))
        return False
    print(json.dumps({"test": "runs_successfully", "passed": True, "message": "process.py runs and produces output.json"}))
    return True


def test_deduplication():
    _clean_outputs()
    _run_process()
    output_path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"test": "deduplication", "passed": False, "message": "output.json not found"}))
        return
    with open(output_path) as f:
        data = json.load(f)
    # Input has 10 records but only 7 unique IDs
    ids = [r["id"] for r in data]
    unique_ids = set(ids)
    if len(ids) != len(unique_ids):
        print(json.dumps({"test": "deduplication", "passed": False, "message": f"Output has {len(ids)} records but only {len(unique_ids)} unique IDs — duplicates not removed"}))
        return
    if len(data) != 7:
        print(json.dumps({"test": "deduplication", "passed": False, "message": f"Expected 7 unique records, got {len(data)}"}))
        return
    print(json.dumps({"test": "deduplication", "passed": True, "message": "Correctly deduplicated: 10 input records -> 7 unique output records"}))


def test_idempotent_output():
    """Run process.py 3 times — output.json should be identical each time."""
    _clean_outputs()
    _run_process()
    output_path = os.path.join(CHALLENGE_DIR, "setup", "output.json")
    with open(output_path) as f:
        first_run = f.read()

    _run_process()
    with open(output_path) as f:
        second_run = f.read()

    _run_process()
    with open(output_path) as f:
        third_run = f.read()

    if first_run == second_run == third_run:
        count = len(json.loads(first_run))
        print(json.dumps({"test": "idempotent_output", "passed": True, "message": f"Output identical across 3 runs ({count} records)"}))
    else:
        c1 = len(json.loads(first_run))
        c2 = len(json.loads(second_run))
        c3 = len(json.loads(third_run))
        print(json.dumps({"test": "idempotent_output", "passed": False, "message": f"Output differs across runs. Record counts: run1={c1}, run2={c2}, run3={c3}"}))


def test_idempotent_state():
    """Run process.py 3 times — state.json should be identical each time."""
    _clean_outputs()
    _run_process()
    state_path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    if not os.path.exists(state_path):
        print(json.dumps({"test": "idempotent_state", "passed": False, "message": "state.json not found after running process.py"}))
        return
    with open(state_path) as f:
        first_state = f.read()

    _run_process()
    with open(state_path) as f:
        second_state = f.read()

    _run_process()
    with open(state_path) as f:
        third_state = f.read()

    if first_state == second_state == third_state:
        print(json.dumps({"test": "idempotent_state", "passed": True, "message": "State identical across 3 runs"}))
    else:
        s1 = json.loads(first_state).get("processed_count", "?")
        s2 = json.loads(second_state).get("processed_count", "?")
        s3 = json.loads(third_state).get("processed_count", "?")
        print(json.dumps({"test": "idempotent_state", "passed": False, "message": f"State differs across runs. processed_count: run1={s1}, run2={s2}, run3={s3}"}))


def test_state_values_correct():
    _clean_outputs()
    _run_process()
    state_path = os.path.join(CHALLENGE_DIR, "setup", "state.json")
    if not os.path.exists(state_path):
        print(json.dumps({"test": "state_values_correct", "passed": False, "message": "state.json not found"}))
        return
    with open(state_path) as f:
        state = json.load(f)
    if state.get("processed_count") != 7:
        print(json.dumps({"test": "state_values_correct", "passed": False, "message": f"processed_count should be 7 (unique records), got {state.get('processed_count')}"}))
        return
    # Total of unique amounts: 150 + 275.5 + 89.99 + 320 + 45.75 + 199.99 + 510 = 1591.23
    expected_total = 1591.23
    actual_total = state.get("total_amount", 0)
    if abs(actual_total - expected_total) > 0.01:
        print(json.dumps({"test": "state_values_correct", "passed": False, "message": f"total_amount should be {expected_total}, got {actual_total}"}))
        return
    print(json.dumps({"test": "state_values_correct", "passed": True, "message": f"State values correct: count=7, total={expected_total}"}))


if __name__ == "__main__":
    test_runs_successfully()
    test_deduplication()
    test_idempotent_output()
    test_idempotent_state()
    test_state_values_correct()
