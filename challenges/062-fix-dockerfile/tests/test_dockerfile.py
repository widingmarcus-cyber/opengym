"""Tests for Challenge 062: Fix Dockerfile."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

DOCKERFILE_PATH = Path(__file__).parent.parent / "setup" / "Dockerfile"


def read_dockerfile():
    return DOCKERFILE_PATH.read_text().strip().splitlines()


def read_dockerfile_upper():
    return [line.strip().upper() for line in read_dockerfile() if line.strip()]


def get_instructions(lines):
    instructions = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            instructions.append(stripped)
    return instructions


def test_from_uses_python3():
    lines = read_dockerfile()
    from_lines = [l for l in lines if l.strip().upper().startswith("FROM")]
    assert len(from_lines) >= 1, "Dockerfile must have a FROM instruction"
    from_line = from_lines[0].strip()
    assert "2.7" not in from_line, "Must not use Python 2.7"
    assert "python:3" in from_line.lower() or "python3" in from_line.lower(), \
        "FROM must reference a Python 3.x image"


def test_from_uses_slim_variant():
    lines = read_dockerfile()
    from_lines = [l for l in lines if l.strip().upper().startswith("FROM")]
    from_line = from_lines[0].strip().lower()
    assert "slim" in from_line, "Should use a slim base image variant"


def test_workdir_before_copy():
    instructions = get_instructions(read_dockerfile())
    workdir_idx = None
    copy_idx = None
    for i, line in enumerate(instructions):
        upper = line.upper()
        if upper.startswith("WORKDIR") and workdir_idx is None:
            workdir_idx = i
        if upper.startswith("COPY") and copy_idx is None:
            copy_idx = i
    assert workdir_idx is not None, "Dockerfile must have a WORKDIR instruction"
    assert copy_idx is not None, "Dockerfile must have a COPY instruction"
    assert workdir_idx < copy_idx, "WORKDIR must come before COPY"


def test_workdir_is_set():
    instructions = get_instructions(read_dockerfile())
    workdir_lines = [l for l in instructions if l.upper().startswith("WORKDIR")]
    assert len(workdir_lines) >= 1, "Must have at least one WORKDIR instruction"
    workdir_path = workdir_lines[0].split(None, 1)[1]
    assert workdir_path.startswith("/"), "WORKDIR should be an absolute path"


def test_pip_install_exists():
    lines = read_dockerfile()
    content = "\n".join(lines).lower()
    assert "pip install" in content, "Dockerfile must include a pip install step"


def test_flask_is_installed():
    lines = read_dockerfile()
    content = "\n".join(lines).lower()
    has_flask_direct = "pip install" in content and "flask" in content
    has_requirements = "requirements.txt" in content and "pip install" in content
    assert has_flask_direct or has_requirements, \
        "Dockerfile must install flask (directly or via requirements.txt)"


def test_cmd_is_valid_syntax():
    instructions = get_instructions(read_dockerfile())
    cmd_lines = [l for l in instructions if l.upper().startswith("CMD")]
    assert len(cmd_lines) >= 1, "Dockerfile must have a CMD instruction"
    cmd_line = cmd_lines[-1]
    cmd_body = cmd_line[3:].strip()
    is_exec_form = cmd_body.startswith("[")
    is_shell_form = not is_exec_form and ("python" in cmd_body.lower())
    assert is_exec_form or is_shell_form, \
        "CMD must be valid exec-form (JSON array) or shell-form"


def test_expose_port():
    instructions = get_instructions(read_dockerfile())
    expose_lines = [l for l in instructions if l.upper().startswith("EXPOSE")]
    assert len(expose_lines) >= 1, "Dockerfile should have an EXPOSE instruction"
    assert "5000" in expose_lines[0], "Should expose port 5000"
