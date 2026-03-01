import json
import os
import sys
import tempfile

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from processor import process_files


def test_regular_files_read():
    """Regular files in data/ should be read successfully."""
    data_dir = os.path.join(CHALLENGE_DIR, "setup", "data")
    results = process_files(data_dir)
    if "report.txt" not in results or results["report.txt"].get("status") != "ok":
        print(json.dumps({"test": "regular_files_read", "passed": False,
                          "message": f"report.txt not read successfully: {results.get('report.txt')}"}))
        return
    if "Quarterly" not in results["report.txt"].get("content", ""):
        print(json.dumps({"test": "regular_files_read", "passed": False,
                          "message": "report.txt content missing expected text"}))
        return
    print(json.dumps({"test": "regular_files_read", "passed": True, "message": "OK"}))


def test_external_symlink_blocked():
    """Symlinks pointing outside data/ must be blocked."""
    data_dir = os.path.join(CHALLENGE_DIR, "setup", "data")
    # Create a temp file outside the data directory
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, dir=tempfile.gettempdir()) as tmp:
        tmp.write("TOP SECRET DATA")
        tmp_path = tmp.name

    symlink_path = os.path.join(data_dir, "evil_link.txt")
    try:
        # Create symlink pointing outside data_dir
        if os.path.exists(symlink_path) or os.path.islink(symlink_path):
            os.remove(symlink_path)
        os.symlink(tmp_path, symlink_path)

        results = process_files(data_dir)
        entry = results.get("evil_link.txt", {})
        if entry.get("status") == "ok" and "TOP SECRET" in entry.get("content", ""):
            print(json.dumps({"test": "external_symlink_blocked", "passed": False,
                              "message": "External symlink was followed and secret data was read"}))
            return
        print(json.dumps({"test": "external_symlink_blocked", "passed": True, "message": "OK"}))
    except OSError as e:
        # On Windows without developer mode, symlink creation may fail
        if "privilege" in str(e).lower() or "1314" in str(e):
            print(json.dumps({"test": "external_symlink_blocked", "passed": True,
                              "message": "Skipped (symlink creation requires elevated privileges on this OS)"}))
        else:
            print(json.dumps({"test": "external_symlink_blocked", "passed": False,
                              "message": f"Unexpected error: {e}"}))
    finally:
        if os.path.islink(symlink_path):
            os.remove(symlink_path)
        os.unlink(tmp_path)


def test_internal_symlink_allowed():
    """Symlinks pointing to files within data/ should still work."""
    data_dir = os.path.join(CHALLENGE_DIR, "setup", "data")
    target = os.path.join(data_dir, "report.txt")
    symlink_path = os.path.join(data_dir, "report_link.txt")
    try:
        if os.path.exists(symlink_path) or os.path.islink(symlink_path):
            os.remove(symlink_path)
        os.symlink(target, symlink_path)

        results = process_files(data_dir)
        entry = results.get("report_link.txt", {})
        if entry.get("status") != "ok" or "Quarterly" not in entry.get("content", ""):
            print(json.dumps({"test": "internal_symlink_allowed", "passed": False,
                              "message": f"Internal symlink should be allowed but got: {entry}"}))
            return
        print(json.dumps({"test": "internal_symlink_allowed", "passed": True, "message": "OK"}))
    except OSError as e:
        if "privilege" in str(e).lower() or "1314" in str(e):
            print(json.dumps({"test": "internal_symlink_allowed", "passed": True,
                              "message": "Skipped (symlink creation requires elevated privileges on this OS)"}))
        else:
            print(json.dumps({"test": "internal_symlink_allowed", "passed": False,
                              "message": f"Unexpected error: {e}"}))
    finally:
        if os.path.islink(symlink_path):
            os.remove(symlink_path)


def test_function_returns_dict():
    """process_files must return a dict."""
    data_dir = os.path.join(CHALLENGE_DIR, "setup", "data")
    results = process_files(data_dir)
    if not isinstance(results, dict):
        print(json.dumps({"test": "function_returns_dict", "passed": False,
                          "message": f"Expected dict, got {type(results).__name__}"}))
        return
    print(json.dumps({"test": "function_returns_dict", "passed": True, "message": "OK"}))


def test_realpath_used_for_validation():
    """The processor code must reference os.path.realpath for symlink resolution."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "processor.py")
    with open(source_path, "r") as f:
        source = f.read()
    if "realpath" not in source:
        print(json.dumps({"test": "realpath_used_for_validation", "passed": False,
                          "message": "processor.py does not use os.path.realpath() for symlink validation"}))
        return
    print(json.dumps({"test": "realpath_used_for_validation", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_regular_files_read()
    test_external_symlink_blocked()
    test_internal_symlink_allowed()
    test_function_returns_dict()
    test_realpath_used_for_validation()
