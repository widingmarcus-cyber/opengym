"""Tests for Challenge 063: Fix GitHub Actions Workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import yaml

CI_PATH = Path(__file__).parent.parent / "setup" / "ci.yml"


def load_workflow():
    content = CI_PATH.read_text()
    return yaml.safe_load(content)


def test_valid_yaml():
    content = CI_PATH.read_text()
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise AssertionError(f"YAML is invalid: {e}")
    assert isinstance(data, dict), "Workflow must be a YAML mapping"


def test_trigger_has_branches():
    data = load_workflow()
    assert "on" in data or True in data, "Workflow must have an 'on' trigger"
    trigger = data.get("on") or data.get(True)
    if isinstance(trigger, dict):
        assert "push" in trigger, "Must trigger on push"
        push_config = trigger["push"]
        assert isinstance(push_config, dict), "Push trigger should have configuration"
        assert "branches" in push_config, "Push trigger must specify branches"
        branches = push_config["branches"]
        assert "main" in branches, "Must trigger on the main branch"
    elif isinstance(trigger, str):
        raise AssertionError("Trigger should specify branches, not just 'push'")


def test_runner_is_current():
    data = load_workflow()
    jobs = data.get("jobs", {})
    assert len(jobs) > 0, "Must have at least one job"
    job = list(jobs.values())[0]
    runs_on = job.get("runs-on", "")
    assert "20.04" not in runs_on, "Runner ubuntu-20.04 is outdated"
    assert "ubuntu" in runs_on.lower(), "Must run on Ubuntu"


def test_has_checkout_step():
    data = load_workflow()
    jobs = data.get("jobs", {})
    job = list(jobs.values())[0]
    steps = job.get("steps", [])
    checkout_steps = [
        s for s in steps
        if isinstance(s.get("uses", ""), str) and "actions/checkout" in s["uses"]
    ]
    assert len(checkout_steps) >= 1, "Must have a checkout step using actions/checkout"


def test_has_python_setup_step():
    data = load_workflow()
    jobs = data.get("jobs", {})
    job = list(jobs.values())[0]
    steps = job.get("steps", [])
    python_steps = [
        s for s in steps
        if isinstance(s.get("uses", ""), str) and "actions/setup-python" in s["uses"]
    ]
    assert len(python_steps) >= 1, "Must have a Python setup step"


def test_has_install_step():
    data = load_workflow()
    jobs = data.get("jobs", {})
    job = list(jobs.values())[0]
    steps = job.get("steps", [])
    install_steps = [
        s for s in steps
        if isinstance(s.get("run", ""), str) and "pip install" in s["run"]
    ]
    assert len(install_steps) >= 1, "Must have a dependency install step"


def test_has_test_step():
    data = load_workflow()
    jobs = data.get("jobs", {})
    job = list(jobs.values())[0]
    steps = job.get("steps", [])
    test_steps = [
        s for s in steps
        if isinstance(s.get("run", ""), str) and "pytest" in s["run"]
    ]
    assert len(test_steps) >= 1, "Must have a test step running pytest"


def test_all_steps_have_uses_or_run():
    data = load_workflow()
    jobs = data.get("jobs", {})
    job = list(jobs.values())[0]
    steps = job.get("steps", [])
    assert len(steps) >= 4, "Must have at least 4 steps"
    for i, step in enumerate(steps):
        has_uses = "uses" in step
        has_run = "run" in step
        assert has_uses or has_run, \
            f"Step {i} ('{step.get('name', 'unnamed')}') must have 'uses' or 'run'"
