"""Hidden tests for Challenge 048: Test the Untestable."""

import sys
import os
import importlib
import inspect
import subprocess
import shutil
import tempfile
from pathlib import Path

# Add setup/ to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

SETUP_DIR = Path(__file__).parent.parent / "setup"
CORRECT_CODE = (SETUP_DIR / "notifier.py").read_text()


def _get_test_functions():
    """Import test_notifier and return all test function names."""
    import test_notifier
    importlib.reload(test_notifier)
    return [name for name in dir(test_notifier) if name.startswith("test_")]


def _run_tests_with_code(notifier_content):
    """Run agent's test_notifier.py against a custom notifier.py."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(SETUP_DIR / "test_notifier.py", Path(tmp) / "test_notifier.py")
        (Path(tmp) / "notifier.py").write_text(notifier_content)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_notifier.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=tmp,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result


# Buggy: send_notification doesn't check for None user
BUGGY_NO_NONE_CHECK = CORRECT_CODE.replace(
    """    if user is None:
        return {"success": False, "error": "User not found"}""",
    """    # no None check"""
)

# Buggy: send_notification doesn't format the message
BUGGY_NO_FORMAT = CORRECT_CODE.replace(
    '''    formatted_message = f"Hello {user['name']}, {message}"''',
    '''    formatted_message = message'''
)

# Buggy: send_notification doesn't handle email failure
BUGGY_NO_EMAIL_ERROR = CORRECT_CODE.replace(
    """    try:
        _send_email(user["email"], formatted_message)
    except Exception:
        return {"success": False, "error": "Email delivery failed"}""",
    """    _send_email(user["email"], formatted_message)"""
)


def test_agent_uses_mock():
    """Agent tests must use unittest.mock.patch."""
    import test_notifier
    importlib.reload(test_notifier)
    source = inspect.getsource(test_notifier)
    assert "patch" in source, (
        "Tests must use unittest.mock.patch to mock dependencies"
    )
    assert "mock" in source.lower(), (
        "Tests must use mocking to isolate the function under test"
    )


def test_at_least_4_test_functions():
    """Agent must write at least 4 test functions."""
    test_fns = _get_test_functions()
    assert len(test_fns) >= 4, (
        f"Expected at least 4 test functions, found {len(test_fns)}: {test_fns}"
    )


def test_agent_tests_pass_correct_code():
    """All agent-written tests must pass against the correct notifier.py."""
    result = _run_tests_with_code(CORRECT_CODE)
    assert result.returncode == 0, (
        f"Agent tests failed against correct code:\n{result.stdout}\n{result.stderr}"
    )


def test_tests_reference_send_notification():
    """Agent tests must test the send_notification function."""
    import test_notifier
    importlib.reload(test_notifier)
    source = inspect.getsource(test_notifier)
    assert "send_notification" in source, (
        "Tests must call send_notification"
    )


def test_tests_mock_get_user():
    """Agent tests must mock _get_user_from_db."""
    import test_notifier
    importlib.reload(test_notifier)
    source = inspect.getsource(test_notifier)
    assert "_get_user_from_db" in source, (
        "Tests must mock _get_user_from_db"
    )


def test_tests_mock_send_email():
    """Agent tests must mock _send_email."""
    import test_notifier
    importlib.reload(test_notifier)
    source = inspect.getsource(test_notifier)
    assert "_send_email" in source, (
        "Tests must mock _send_email"
    )


def test_agent_tests_detect_no_format_bug():
    """Agent tests should detect when message formatting is skipped."""
    result = _run_tests_with_code(BUGGY_NO_FORMAT)
    assert result.returncode != 0, (
        "Agent tests did not detect the missing message formatting bug"
    )


def test_agent_tests_detect_email_error_bug():
    """Agent tests should detect when email failure handling is broken."""
    result = _run_tests_with_code(BUGGY_NO_EMAIL_ERROR)
    assert result.returncode != 0, (
        "Agent tests did not detect the missing email error handling bug"
    )
