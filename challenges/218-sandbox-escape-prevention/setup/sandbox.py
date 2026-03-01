"""
Code sandbox module.
VULNERABILITY: The sandbox has multiple gaps that allow escape via
subprocess, dynamic imports, and unrestricted builtins.
"""

import ast


def run_sandboxed(code_string):
    """
    Execute user-supplied Python code in a restricted environment.

    Args:
        code_string: A string of Python code to execute.

    Returns:
        dict with "status" and either "result" or "message"
    """
    # Weak blocklist check — only blocks literal "import os" text
    if "import os" in code_string:
        return {"status": "blocked", "message": "Importing os is not allowed"}

    if "open(" in code_string:
        return {"status": "blocked", "message": "File I/O is not allowed"}

    # BUG: No restriction on __import__, importlib, subprocess, sys, eval, exec
    # BUG: Full builtins are available — should use allowlist
    try:
        result = {}
        exec(code_string, {"__builtins__": __builtins__}, result)
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
