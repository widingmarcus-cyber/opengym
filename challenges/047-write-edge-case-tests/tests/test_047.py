"""Hidden tests for Challenge 047: Write Edge Case Tests."""

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
CORRECT_CODE = (SETUP_DIR / "string_utils.py").read_text()


def _get_test_functions():
    """Import test_edge_cases and return all test function names."""
    import test_edge_cases
    importlib.reload(test_edge_cases)
    return [name for name in dir(test_edge_cases) if name.startswith("test_")]


def _run_tests_with_code(string_utils_content):
    """Run agent's test_edge_cases.py against a custom string_utils.py."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(SETUP_DIR / "test_edge_cases.py", Path(tmp) / "test_edge_cases.py")
        (Path(tmp) / "string_utils.py").write_text(string_utils_content)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_edge_cases.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=tmp,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result


def _assert_tests_detect_bug(buggy_code, bug_description):
    """Verify that agent's tests actually FAIL (not just 'no tests collected') on buggy code."""
    # First ensure agent's tests pass on correct code
    correct_result = _run_tests_with_code(CORRECT_CODE)
    assert correct_result.returncode == 0, (
        f"Agent tests must pass on correct code before checking bug detection:\n"
        f"{correct_result.stdout}\n{correct_result.stderr}"
    )
    # Then check that they fail on buggy code with actual FAILED tests
    buggy_result = _run_tests_with_code(buggy_code)
    assert buggy_result.returncode != 0, (
        f"Agent tests did not detect {bug_description}"
    )
    output = buggy_result.stdout + buggy_result.stderr
    assert "FAILED" in output or "failed" in output.lower().split("=")[-1], (
        f"Agent tests exited non-zero but no test failures detected for {bug_description}. "
        f"Tests may be empty or not collecting. Output:\n{output}"
    )


# Buggy: wrap_text doesn't handle empty string (returns text instead of "")
BUGGY_WRAP_EMPTY = CORRECT_CODE.replace(
    '''    if not text:
        return ""
    if width <= 0:
        return text''',
    '''    if width <= 0:
        return text'''
)

# Buggy: pad_center ignores the char parameter
BUGGY_PAD_CHAR = CORRECT_CODE.replace(
    "return char * left_padding + text + char * right_padding",
    'return " " * left_padding + text + " " * right_padding'
)

# Buggy: remove_duplicates fails on empty string (crashes)
BUGGY_REMOVE_EMPTY = CORRECT_CODE.replace(
    '''    if not text:
        return ""
    result = [text[0]]''',
    '''    result = [text[0]]'''
)

# Buggy: count_words counts empty strings as 1 word
BUGGY_COUNT_EMPTY = CORRECT_CODE.replace(
    "return len(text.split())",
    'return max(1, len(text.split()))'
)

# Buggy: wrap_text doesn't handle width=0 correctly (infinite loop or wrong result)
BUGGY_WRAP_ZERO_WIDTH = CORRECT_CODE.replace(
    '''    if width <= 0:
        return text''',
    '''    if width < 0:
        return text'''
)

# Buggy: pad_center doesn't handle single-char text correctly (off by one in padding)
BUGGY_PAD_ODD = CORRECT_CODE.replace(
    "left_padding = total_padding // 2\n    right_padding = total_padding - left_padding",
    "left_padding = total_padding // 2\n    right_padding = total_padding // 2"
)


def test_at_least_12_test_functions():
    """The agent must write at least 12 test functions."""
    test_fns = _get_test_functions()
    assert len(test_fns) >= 12, (
        f"Expected at least 12 test functions, found {len(test_fns)}: {test_fns}"
    )


def test_tests_cover_all_functions():
    """The agent's tests should reference all four string utility functions."""
    import test_edge_cases
    importlib.reload(test_edge_cases)
    source = inspect.getsource(test_edge_cases)
    for fn_name in ["wrap_text", "pad_center", "remove_duplicates", "count_words"]:
        assert fn_name in source, (
            f"Tests should cover '{fn_name}' but it was not found in test source"
        )


def test_agent_tests_pass_correct_code():
    """All agent-written tests must pass against the correct string_utils.py."""
    result = _run_tests_with_code(CORRECT_CODE)
    assert result.returncode == 0, (
        f"Agent tests failed against correct code:\n{result.stdout}\n{result.stderr}"
    )


def test_agent_tests_detect_wrap_empty_bug():
    """Agent tests should detect the wrap_text empty string bug."""
    _assert_tests_detect_bug(BUGGY_WRAP_EMPTY, "the wrap_text empty string handling bug")


def test_agent_tests_detect_pad_char_bug():
    """Agent tests should detect the pad_center custom char bug."""
    _assert_tests_detect_bug(BUGGY_PAD_CHAR, "the pad_center custom char bug")


def test_agent_tests_detect_remove_empty_bug():
    """Agent tests should detect the remove_duplicates empty string bug."""
    _assert_tests_detect_bug(BUGGY_REMOVE_EMPTY, "the remove_duplicates empty string crash bug")


def test_agent_tests_detect_count_empty_bug():
    """Agent tests should detect the count_words empty string bug."""
    _assert_tests_detect_bug(BUGGY_COUNT_EMPTY, "the count_words empty string bug")


def test_edge_cases_in_test_source():
    """Agent tests should include actual edge case testing (empty strings, etc.)."""
    import test_edge_cases
    importlib.reload(test_edge_cases)
    source = inspect.getsource(test_edge_cases)
    edge_indicators = ['""', "''", "empty", "edge", "boundary", "zero", "single"]
    found = sum(1 for indicator in edge_indicators if indicator in source.lower())
    assert found >= 2, (
        "Tests should include edge cases like empty strings, but found few edge case indicators"
    )


def test_agent_tests_detect_wrap_zero_width_bug():
    """Agent tests should detect the wrap_text zero-width bug."""
    _assert_tests_detect_bug(
        BUGGY_WRAP_ZERO_WIDTH, "the wrap_text zero-width handling bug"
    )


def test_agent_tests_detect_pad_odd_width_bug():
    """Agent tests should detect the pad_center odd padding bug."""
    _assert_tests_detect_bug(
        BUGGY_PAD_ODD, "the pad_center odd-width padding distribution bug"
    )
