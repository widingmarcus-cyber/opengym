"""Tests for Challenge 068: Write CI Pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import yaml

PIPELINE_PATH = Path(__file__).parent.parent / "setup" / "pipeline.yml"


def load_pipeline():
    content = PIPELINE_PATH.read_text()
    return yaml.safe_load(content)


def test_valid_yaml():
    content = PIPELINE_PATH.read_text()
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise AssertionError(f"YAML is invalid: {e}")
    assert isinstance(data, dict), "Pipeline must be a valid YAML mapping"


def test_triggers_configured():
    data = load_pipeline()
    trigger = data.get("on") or data.get(True)
    assert trigger is not None, "Must have 'on' trigger"
    assert isinstance(trigger, dict), "Trigger must be a mapping"
    assert "push" in trigger, "Must trigger on push"
    push = trigger["push"]
    assert "branches" in push, "Push must specify branches"
    assert "main" in push["branches"], "Push must trigger on main"
    assert "pull_request" in trigger, "Must trigger on pull_request"


def test_matrix_strategy():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    test_job = jobs.get("test", {})
    strategy = test_job.get("strategy", {})
    matrix = strategy.get("matrix", {})
    python_key = None
    for key in matrix:
        if "python" in key.lower():
            python_key = key
            break
    assert python_key is not None, "Matrix must include python version key"
    versions = [str(v) for v in matrix[python_key]]
    assert "3.10" in versions or "3.10" in str(versions), "Matrix must include Python 3.10"
    assert "3.11" in versions or "3.11" in str(versions), "Matrix must include Python 3.11"
    assert "3.12" in versions or "3.12" in str(versions), "Matrix must include Python 3.12"


def test_caching_step():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    test_job = jobs.get("test", {})
    steps = test_job.get("steps", [])
    cache_steps = [
        s for s in steps
        if isinstance(s.get("uses", ""), str) and "actions/cache" in s["uses"]
    ]
    assert len(cache_steps) >= 1, "Must have a caching step using actions/cache"
    cache_step = cache_steps[0]
    with_block = cache_step.get("with", {})
    assert "path" in with_block, "Cache step must specify path"
    assert "key" in with_block, "Cache step must specify key"


def test_test_step():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    test_job = jobs.get("test", {})
    steps = test_job.get("steps", [])
    test_steps = [
        s for s in steps
        if isinstance(s.get("run", ""), str) and "pytest" in s["run"]
    ]
    assert len(test_steps) >= 1, "Must have a test step running pytest"
    run_cmd = test_steps[0]["run"]
    assert "--cov" in run_cmd, "Test command must include coverage"


def test_coverage_artifact_upload():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    test_job = jobs.get("test", {})
    steps = test_job.get("steps", [])
    upload_steps = [
        s for s in steps
        if isinstance(s.get("uses", ""), str) and "upload-artifact" in s["uses"]
    ]
    assert len(upload_steps) >= 1, "Must have an artifact upload step"
    with_block = upload_steps[0].get("with", {})
    assert "name" in with_block, "Upload step must specify artifact name"
    assert "path" in with_block, "Upload step must specify artifact path"


def test_deploy_job_exists():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    assert "deploy" in jobs, "Must have a deploy job"
    deploy = jobs["deploy"]
    needs = deploy.get("needs", [])
    if isinstance(needs, str):
        needs = [needs]
    assert "test" in needs, "Deploy must need test job"


def test_deploy_conditional():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    deploy = jobs.get("deploy", {})
    condition = deploy.get("if", "")
    assert "main" in str(condition) or "github.ref" in str(condition) or \
           "github.event_name" in str(condition), \
        "Deploy must have a condition limiting it to main branch pushes"


def test_deploy_has_steps():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    deploy = jobs.get("deploy", {})
    steps = deploy.get("steps", [])
    assert len(steps) >= 3, "Deploy must have at least 3 steps"
    deploy_steps = [
        s for s in steps
        if isinstance(s.get("run", ""), str) and "deploy" in s["run"].lower()
    ]
    assert len(deploy_steps) >= 1, "Deploy must have a deployment step"


def test_both_jobs_use_ubuntu():
    data = load_pipeline()
    jobs = data.get("jobs", {})
    for job_name, job_config in jobs.items():
        runs_on = job_config.get("runs-on", "")
        assert "ubuntu" in str(runs_on).lower(), \
            f"Job '{job_name}' must run on Ubuntu"
