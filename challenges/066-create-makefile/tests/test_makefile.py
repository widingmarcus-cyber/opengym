"""Tests for Challenge 066: Create Makefile."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

MAKEFILE_PATH = Path(__file__).parent.parent / "setup" / "Makefile"


def read_makefile():
    return MAKEFILE_PATH.read_text()


def get_targets(content):
    return re.findall(r"^([a-zA-Z_][a-zA-Z0-9_-]*):", content, re.MULTILINE)


def test_all_targets_exist():
    content = read_makefile()
    targets = get_targets(content)
    required = ["install", "test", "lint", "format", "clean", "build", "deploy"]
    for target in required:
        assert target in targets, f"Missing target: {target}"


def test_phony_declarations():
    content = read_makefile()
    phony_matches = re.findall(r"\.PHONY\s*:(.*)", content)
    phony_all = " ".join(phony_matches)
    required = ["install", "test", "lint", "format", "clean", "build", "deploy"]
    for target in required:
        assert target in phony_all, f"Target '{target}' must be declared as .PHONY"


def test_install_command():
    content = read_makefile()
    assert "pip install" in content, "install target must run pip install"


def test_test_command():
    content = read_makefile()
    assert "pytest" in content, "test target must run pytest"


def test_deploy_depends_on_test():
    content = read_makefile()
    deploy_match = re.search(r"^deploy\s*:(.*)", content, re.MULTILINE)
    assert deploy_match, "deploy target must exist"
    deps = deploy_match.group(1)
    assert "test" in deps, "deploy must depend on test"


def test_deploy_depends_on_build():
    content = read_makefile()
    deploy_match = re.search(r"^deploy\s*:(.*)", content, re.MULTILINE)
    assert deploy_match, "deploy target must exist"
    deps = deploy_match.group(1)
    assert "build" in deps, "deploy must depend on build"


def test_build_depends_on_test_and_lint():
    content = read_makefile()
    build_match = re.search(r"^build\s*:(.*)", content, re.MULTILINE)
    assert build_match, "build target must exist"
    deps = build_match.group(1)
    assert "test" in deps, "build must depend on test"
    assert "lint" in deps, "build must depend on lint"


def test_clean_command():
    content = read_makefile()
    assert "rm -rf" in content or "rm -r" in content, \
        "clean target must remove build artifacts"
