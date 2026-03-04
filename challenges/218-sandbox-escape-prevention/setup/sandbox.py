"""
Code sandbox module.
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
    if "import os" in code_string:
        return {"status": "blocked", "message": "Importing os is not allowed"}

    if "open(" in code_string:
        return {"status": "blocked", "message": "File I/O is not allowed"}

    try:
        result = {}
        exec(code_string, {"__builtins__": __builtins__}, result)
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
