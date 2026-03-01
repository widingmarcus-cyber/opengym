"""Hidden tests for Challenge 049: Property-Based Testing."""

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
CORRECT_CODE = (SETUP_DIR / "serializer.py").read_text()


def _get_test_functions():
    """Import test_properties and return all test function names."""
    import test_properties
    importlib.reload(test_properties)
    return [name for name in dir(test_properties) if name.startswith("test_")]


def _run_tests_with_code(serializer_content):
    """Run agent's test_properties.py against a custom serializer.py."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(SETUP_DIR / "test_properties.py", Path(tmp) / "test_properties.py")
        (Path(tmp) / "serializer.py").write_text(serializer_content)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_properties.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=tmp,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result


# Buggy: encode doesn't distinguish bool from int
BUGGY_BOOL_INT = CORRECT_CODE.replace(
    """    if isinstance(data, bool):
        return f"B:{'1' if data else '0'}"
    if isinstance(data, int):""",
    """    if isinstance(data, int):"""
)

# Buggy: decode float returns int when value is whole number
BUGGY_FLOAT = CORRECT_CODE.replace(
    '''    if type_tag == "F:":
        return float(payload)''',
    '''    if type_tag == "F:":
        val = float(payload)
        return int(val) if val == int(val) else val'''
)


def test_at_least_6_test_functions():
    """Agent must write at least 6 test functions."""
    test_fns = _get_test_functions()
    assert len(test_fns) >= 6, (
        f"Expected at least 6 test functions, found {len(test_fns)}: {test_fns}"
    )


def test_tests_reference_encode_and_decode():
    """Agent tests must use both encode and decode."""
    import test_properties
    importlib.reload(test_properties)
    source = inspect.getsource(test_properties)
    assert "encode" in source, "Tests must use the encode function"
    assert "decode" in source, "Tests must use the decode function"


def test_tests_use_multiple_inputs():
    """Agent tests should test multiple inputs (loops or many assertions)."""
    import test_properties
    importlib.reload(test_properties)
    source = inspect.getsource(test_properties)
    has_loop = "for " in source
    assertion_count = source.count("assert ")
    assert has_loop or assertion_count >= 10, (
        "Property tests should use loops or many assertions to test multiple inputs"
    )


def test_agent_tests_pass_correct_code():
    """All agent-written tests must pass against the correct serializer.py."""
    result = _run_tests_with_code(CORRECT_CODE)
    assert result.returncode == 0, (
        f"Agent tests failed against correct code:\n{result.stdout}\n{result.stderr}"
    )


def test_agent_tests_detect_bool_int_bug():
    """Agent tests should detect when booleans are encoded as integers."""
    result = _run_tests_with_code(BUGGY_BOOL_INT)
    assert result.returncode != 0, (
        "Agent tests did not detect the bool/int confusion bug"
    )


def test_agent_tests_detect_float_bug():
    """Agent tests should detect when whole floats are decoded as ints."""
    result = _run_tests_with_code(BUGGY_FLOAT)
    assert result.returncode != 0, (
        "Agent tests did not detect the float-to-int conversion bug"
    )
