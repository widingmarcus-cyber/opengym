import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from sandbox import run_sandboxed


def test_safe_arithmetic():
    """Safe arithmetic operations should work in the sandbox."""
    result = run_sandboxed("answer = 2 + 3 * 4")
    if result.get("status") != "ok":
        print(json.dumps({"test": "safe_arithmetic", "passed": False,
                          "message": f"Safe arithmetic was blocked: {result}"}))
        return
    if result.get("result", {}).get("answer") != 14:
        print(json.dumps({"test": "safe_arithmetic", "passed": False,
                          "message": f"Expected answer=14, got: {result}"}))
        return
    print(json.dumps({"test": "safe_arithmetic", "passed": True, "message": "OK"}))


def test_safe_builtins_work():
    """Safe builtins like len, sorted, range should work."""
    result = run_sandboxed("answer = len([1,2,3])")
    if result.get("status") != "ok" or result.get("result", {}).get("answer") != 3:
        print(json.dumps({"test": "safe_builtins_work", "passed": False,
                          "message": f"len() failed: {result}"}))
        return
    result2 = run_sandboxed("answer = sorted([3,1,2])")
    if result2.get("status") != "ok" or result2.get("result", {}).get("answer") != [1, 2, 3]:
        print(json.dumps({"test": "safe_builtins_work", "passed": False,
                          "message": f"sorted() failed: {result2}"}))
        return
    print(json.dumps({"test": "safe_builtins_work", "passed": True, "message": "OK"}))


def test_dunder_import_blocked():
    """__import__('os') and __import__('subprocess') must be blocked."""
    result = run_sandboxed("m = __import__('os')\nanswer = m.getcwd()")
    if result.get("status") == "ok":
        print(json.dumps({"test": "dunder_import_blocked", "passed": False,
                          "message": f"__import__('os') was NOT blocked: {result}"}))
        return
    result2 = run_sandboxed("m = __import__('subprocess')\nanswer = m.check_output(['echo','pwned'])")
    if result2.get("status") == "ok":
        print(json.dumps({"test": "dunder_import_blocked", "passed": False,
                          "message": f"__import__('subprocess') was NOT blocked: {result2}"}))
        return
    print(json.dumps({"test": "dunder_import_blocked", "passed": True, "message": "OK"}))


def test_eval_exec_blocked():
    """eval() and exec() within sandboxed code must be blocked."""
    result = run_sandboxed("answer = eval('__import__(\"os\").getcwd()')")
    if result.get("status") == "ok":
        print(json.dumps({"test": "eval_exec_blocked", "passed": False,
                          "message": f"eval() within sandbox was NOT blocked: {result}"}))
        return
    result2 = run_sandboxed("exec('import subprocess')")
    if result2.get("status") == "ok":
        print(json.dumps({"test": "eval_exec_blocked", "passed": False,
                          "message": f"exec() within sandbox was NOT blocked: {result2}"}))
        return
    print(json.dumps({"test": "eval_exec_blocked", "passed": True, "message": "OK"}))


def test_allowlist_approach():
    """The sandbox source must use an allowlist for builtins, not the full __builtins__."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "sandbox.py")
    with open(source_path, "r") as f:
        source = f.read()
    # Check that the code doesn't just pass __builtins__ directly
    if '"__builtins__": __builtins__' in source or "'__builtins__': __builtins__" in source:
        print(json.dumps({"test": "allowlist_approach", "passed": False,
                          "message": "Sandbox still passes full __builtins__ — must use an allowlist"}))
        return
    # Check for evidence of an allowlist (dict with specific safe builtins)
    if "len" not in source or "range" not in source:
        print(json.dumps({"test": "allowlist_approach", "passed": False,
                          "message": "No evidence of a builtins allowlist in sandbox code"}))
        return
    print(json.dumps({"test": "allowlist_approach", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_safe_arithmetic()
    test_safe_builtins_work()
    test_dunder_import_blocked()
    test_eval_exec_blocked()
    test_allowlist_approach()
