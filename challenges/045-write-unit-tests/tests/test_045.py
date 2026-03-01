"""Hidden tests for Challenge 045: Write Unit Tests."""

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


def _get_test_functions():
    """Import test_utils and return all test function names."""
    import test_utils
    importlib.reload(test_utils)
    return [name for name in dir(test_utils) if name.startswith("test_")]


def _run_tests_with_utils(utils_content):
    """Run agent's test_utils.py against a custom utils.py in a temp dir."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(SETUP_DIR / "test_utils.py", Path(tmp) / "test_utils.py")
        (Path(tmp) / "utils.py").write_text(utils_content)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_utils.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=tmp,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result


def _assert_tests_detect_bug(buggy_code, bug_description):
    """Verify that agent's tests actually FAIL (not just 'no tests collected') on buggy code."""
    # First ensure agent's tests pass on correct code
    correct_result = _run_tests_with_utils(CORRECT_UTILS)
    assert correct_result.returncode == 0, (
        f"Agent tests must pass on correct code before checking bug detection:\n"
        f"{correct_result.stdout}\n{correct_result.stderr}"
    )
    # Then check that they fail on buggy code with actual FAILED tests
    buggy_result = _run_tests_with_utils(buggy_code)
    assert buggy_result.returncode != 0, (
        f"Agent tests did not detect {bug_description}"
    )
    output = buggy_result.stdout + buggy_result.stderr
    assert "FAILED" in output or "failed" in output.lower().split("=")[-1], (
        f"Agent tests exited non-zero but no test failures detected for {bug_description}. "
        f"Tests may be empty or not collecting. Output:\n{output}"
    )


CORRECT_UTILS = (SETUP_DIR / "utils.py").read_text()

BUGGY_SLUGIFY = CORRECT_UTILS.replace(
    "text = text.lower().strip()",
    "text = text.strip()"
)

BUGGY_TRUNCATE = CORRECT_UTILS.replace(
    "return text[:max_len - len(suffix)] + suffix",
    "return text[:max_len] + suffix"
)

BUGGY_IS_VALID_URL = CORRECT_UTILS.replace(
    r"r'^https?://'",
    r"r'^(https?|ftp)://'"
)

BUGGY_DEEP_MERGE = CORRECT_UTILS.replace(
    """    for key, value in dict_b.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result""",
    """    result.update(dict_b)
    return result"""
)

BUGGY_CHUNK_LIST = CORRECT_UTILS.replace(
    """    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i:i + size] for i in range(0, len(lst), size)]""",
    """    return [lst[i:i + size] for i in range(0, len(lst), size)]"""
)


def test_at_least_10_test_functions():
    """The agent must write at least 10 test functions."""
    test_fns = _get_test_functions()
    assert len(test_fns) >= 10, (
        f"Expected at least 10 test functions, found {len(test_fns)}: {test_fns}"
    )


def test_tests_cover_all_functions():
    """The agent's tests should reference all five utility functions."""
    import test_utils
    importlib.reload(test_utils)
    source = inspect.getsource(test_utils)
    for fn_name in ["slugify", "truncate", "is_valid_url", "deep_merge", "chunk_list"]:
        assert fn_name in source, (
            f"Tests should cover the '{fn_name}' function but it was not found in test source"
        )


def test_agent_tests_pass_correct_code():
    """All agent-written tests must pass against the correct utils.py."""
    result = _run_tests_with_utils(CORRECT_UTILS)
    assert result.returncode == 0, (
        f"Agent tests failed against correct code:\n{result.stdout}\n{result.stderr}"
    )


def test_agent_tests_detect_slugify_bug():
    """Agent tests should detect the slugify bug (no lowercasing)."""
    _assert_tests_detect_bug(BUGGY_SLUGIFY, "the slugify lowercasing bug")


def test_agent_tests_detect_truncate_bug():
    """Agent tests should detect the truncate bug (wrong length)."""
    _assert_tests_detect_bug(BUGGY_TRUNCATE, "the truncate off-by-one bug")


def test_agent_tests_detect_deep_merge_bug():
    """Agent tests should detect the deep_merge bug (shallow merge)."""
    _assert_tests_detect_bug(BUGGY_DEEP_MERGE, "the deep_merge shallow merge bug")


def test_agent_tests_detect_is_valid_url_bug():
    """Agent tests should detect the is_valid_url bug (accepts ftp://)."""
    _assert_tests_detect_bug(BUGGY_IS_VALID_URL, "the is_valid_url ftp:// acceptance bug")


def test_agent_tests_detect_chunk_list_bug():
    """Agent tests should detect the chunk_list bug (no ValueError on size<=0)."""
    _assert_tests_detect_bug(BUGGY_CHUNK_LIST, "the chunk_list missing ValueError bug")
