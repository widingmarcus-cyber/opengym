"""Tests for Challenge 030: Trace the Data Corruption."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from app.config import get_config, DEFAULT_CONFIG
from app.loader import load_data
from app.transformer import transform_data
from app.validator import validate_data
from app.reporter import generate_report


def run_pipeline(raw_values):
    """Run the full pipeline and return (values, validation, report)."""
    config = get_config()
    loaded = load_data(raw_values, config)
    transformed = transform_data(loaded, config)
    validation = validate_data(transformed, config)
    report = generate_report(transformed, validation, config)
    return transformed, validation, report


def test_config_not_mutated_after_pipeline():
    """The DEFAULT_CONFIG must not be changed after running the pipeline."""
    original_scale = DEFAULT_CONFIG["scale_factor"]
    original_filters = DEFAULT_CONFIG["filters"]["remove_negatives"]
    run_pipeline([10, 20, 30])
    assert DEFAULT_CONFIG["scale_factor"] == original_scale, \
        f"scale_factor was mutated: expected {original_scale}, got {DEFAULT_CONFIG['scale_factor']}"
    assert DEFAULT_CONFIG["filters"]["remove_negatives"] == original_filters, \
        "filters.remove_negatives was mutated"


def test_config_stable_across_runs():
    """Running the pipeline twice should produce the same results."""
    _, _, report1 = run_pipeline([10, 20, 30])
    _, _, report2 = run_pipeline([10, 20, 30])
    assert report1 == report2, f"Results differ between runs:\nRun 1: {report1}\nRun 2: {report2}"


def test_basic_pipeline_values():
    """Pipeline should produce correct transformed values."""
    values, _, _ = run_pipeline([10, 20, 30, -5, 0])
    assert -5 not in values, "Negatives should be removed"
    assert 0 in values, "Zeros should not be removed by default"
    assert 10 in values
    assert 20 in values
    assert 30 in values


def test_validation_all_valid():
    """Values within range should pass validation."""
    _, validation, _ = run_pipeline([10, 20, 30])
    assert validation["valid"] is True
    assert validation["out_of_range"] == []


def test_capping_at_max():
    """Values above max_threshold should be capped."""
    values, _, _ = run_pipeline([50, 150, 200])
    assert all(v <= 100.0 for v in values), f"Values not capped: {values}"


def test_report_correct_totals():
    """Report should have correct total and average."""
    _, _, report = run_pipeline([10, 20, 30])
    assert report["count"] == 3
    assert report["total"] == 60.0
    assert report["average"] == 20.0
    assert report["is_valid"] is True


def test_scale_factor_in_report():
    """Report should show the original scale_factor (1.0)."""
    _, _, report = run_pipeline([10, 20, 30])
    assert report["scale_factor_used"] == 1.0


def test_negative_filtering_consistent():
    """Negative filtering should work on every run, not just the first."""
    values1, _, _ = run_pipeline([10, -5, 20, -3])
    values2, _, _ = run_pipeline([10, -5, 20, -3])
    assert values1 == values2, f"Filtering differs between runs: {values1} vs {values2}"
    assert all(v >= 0 for v in values1), f"Negatives not filtered: {values1}"
    assert all(v >= 0 for v in values2), f"Negatives not filtered on second run: {values2}"


def test_default_config_scale_factor_is_one():
    """DEFAULT_CONFIG scale_factor must always be 1.0 — it must never be mutated."""
    run_pipeline([10, -5, 20, -3])  # negatives get filtered, changing len(result)/len(values)
    assert DEFAULT_CONFIG["scale_factor"] == 1.0, \
        f"DEFAULT_CONFIG['scale_factor'] was mutated to {DEFAULT_CONFIG['scale_factor']}, expected 1.0"


def test_default_config_remove_negatives_stays_true():
    """DEFAULT_CONFIG filters.remove_negatives must always be True — it must never be mutated."""
    run_pipeline([10, -5, 20])
    assert DEFAULT_CONFIG["filters"]["remove_negatives"] is True, \
        f"DEFAULT_CONFIG['filters']['remove_negatives'] was mutated to {DEFAULT_CONFIG['filters']['remove_negatives']}, expected True"


def test_pipeline_twice_config_unchanged():
    """Call the pipeline twice and verify DEFAULT_CONFIG hasn't changed between calls."""
    import copy
    snapshot_before = copy.deepcopy(DEFAULT_CONFIG)
    run_pipeline([10, -5, 20, -3])  # input with negatives to trigger scale_factor change
    snapshot_after_first = copy.deepcopy(DEFAULT_CONFIG)
    assert snapshot_before == snapshot_after_first, \
        f"DEFAULT_CONFIG mutated after first run: {snapshot_before} -> {snapshot_after_first}"
    run_pipeline([40, -10, 50, 60])
    snapshot_after_second = copy.deepcopy(DEFAULT_CONFIG)
    assert snapshot_before == snapshot_after_second, \
        f"DEFAULT_CONFIG mutated after second run: {snapshot_before} -> {snapshot_after_second}"


def test_get_config_returns_copy_not_same_object():
    """get_config() must return a new dict, not the DEFAULT_CONFIG singleton."""
    cfg = get_config()
    assert cfg is not DEFAULT_CONFIG, (
        "get_config() returns the same object as DEFAULT_CONFIG. "
        "It should return a copy so callers cannot mutate the defaults."
    )


def test_get_config_returns_new_dict_each_call():
    """Two calls to get_config() must return separate objects."""
    cfg1 = get_config()
    cfg2 = get_config()
    assert cfg1 is not cfg2, (
        "get_config() returns the same object on every call. "
        "Each call should return an independent copy."
    )


def test_get_config_filters_is_deep_copy():
    """get_config()['filters'] must not be the same object as DEFAULT_CONFIG['filters']."""
    cfg = get_config()
    assert cfg.get("filters") is not DEFAULT_CONFIG["filters"], (
        "get_config()['filters'] is the same object as DEFAULT_CONFIG['filters']. "
        "A shallow copy is not enough — nested dicts must also be copied."
    )


def test_transform_does_not_mutate_input_config():
    """transform_data must not modify the config dict passed to it."""
    import copy
    config = {
        "scale_factor": 1.0,
        "min_threshold": 0.0,
        "max_threshold": 100.0,
        "precision": 2,
        "filters": {"remove_negatives": True, "remove_zeros": False, "cap_at_max": True},
    }
    original = copy.deepcopy(config)
    transform_data([10, -5, 20], config)
    assert config == original, (
        f"transform_data mutated the config dict: {original} -> {config}"
    )
