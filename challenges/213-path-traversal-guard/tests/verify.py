import json
import os
import sys
import tempfile

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from server import serve_file


def test_legitimate_file_access():
    """Legitimate file requests within files/ should succeed."""
    base_dir = os.path.join(CHALLENGE_DIR, "setup", "files")
    result = serve_file(base_dir, "hello.txt")
    if result.get("status") != "ok" or "Hello" not in result.get("content", ""):
        print(json.dumps({"test": "legitimate_file_access", "passed": False,
                          "message": f"Expected successful read of hello.txt, got: {result}"}))
        return
    print(json.dumps({"test": "legitimate_file_access", "passed": True, "message": "OK"}))


def test_dot_dot_traversal_blocked():
    """Path traversal with ../ sequences must be blocked."""
    base_dir = os.path.join(CHALLENGE_DIR, "setup", "files")
    result = serve_file(base_dir, "../../metadata.yaml")
    if result.get("status") != "error":
        print(json.dumps({"test": "dot_dot_traversal_blocked", "passed": False,
                          "message": f"Path traversal with ../../ was NOT blocked. Got: {result}"}))
        return
    print(json.dumps({"test": "dot_dot_traversal_blocked", "passed": True, "message": "OK"}))


def test_absolute_path_blocked():
    """Absolute paths must be rejected."""
    base_dir = os.path.join(CHALLENGE_DIR, "setup", "files")
    # Create a temp file to ensure an absolute path that exists
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("secret")
        tmp_path = tmp.name
    try:
        result = serve_file(base_dir, tmp_path)
        if result.get("status") != "error":
            print(json.dumps({"test": "absolute_path_blocked", "passed": False,
                              "message": f"Absolute path was NOT blocked. Got: {result}"}))
            return
        print(json.dumps({"test": "absolute_path_blocked", "passed": True, "message": "OK"}))
    finally:
        os.unlink(tmp_path)


def test_encoded_traversal_blocked():
    """Encoded or tricky traversal patterns must be blocked."""
    base_dir = os.path.join(CHALLENGE_DIR, "setup", "files")
    tricky_paths = [
        "../setup/server.py",
        "hello.txt/../../setup/server.py",
        "..\\setup\\server.py",
    ]
    for tricky in tricky_paths:
        result = serve_file(base_dir, tricky)
        if result.get("status") != "error":
            print(json.dumps({"test": "encoded_traversal_blocked", "passed": False,
                              "message": f"Tricky traversal '{tricky}' was NOT blocked. Got: {result}"}))
            return
    print(json.dumps({"test": "encoded_traversal_blocked", "passed": True, "message": "OK"}))


def test_nonexistent_file_still_errors():
    """Requesting a file that doesn't exist should return an error (not crash)."""
    base_dir = os.path.join(CHALLENGE_DIR, "setup", "files")
    result = serve_file(base_dir, "does_not_exist.txt")
    if result.get("status") != "error":
        print(json.dumps({"test": "nonexistent_file_still_errors", "passed": False,
                          "message": f"Expected error for missing file, got: {result}"}))
        return
    print(json.dumps({"test": "nonexistent_file_still_errors", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_legitimate_file_access()
    test_dot_dot_traversal_blocked()
    test_absolute_path_blocked()
    test_encoded_traversal_blocked()
    test_nonexistent_file_still_errors()
