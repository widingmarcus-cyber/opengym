"""Diagnosis of the pipeline crash.

Read the crash log (crash_log.txt) and the source code (app.py),
then fill in each function below with the correct answer.
"""


def get_error_type():
    """Return the exact Python exception type that was raised.

    Example: "ValueError", "KeyError", etc.
    """
    return ""


def get_root_cause_file():
    """Return the filename where the root cause of the bug is.

    This is the file containing the function whose behavior leads
    to the crash (not necessarily where the exception is raised).
    """
    return ""


def get_root_cause_line():
    """Return the line number in the source file where the root cause is.

    This is the line (or start of the function) that should be changed
    to fix the bug. The root cause is in parse_metadata().
    """
    return 0


def get_fix_description():
    """Return a short description of how to fix the bug.

    Your description must mention that the function should 'raise' an
    'exception' instead of returning None silently.
    """
    return ""
