"""Tests for Challenge 096: Feature Flag Rollout."""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from flags import FeatureFlags
from app import new_dashboard, dark_mode, export_csv

CONFIG_PATH = str(Path(__file__).parent.parent / "setup" / "config.json")


def test_enable_and_check():
    ff = FeatureFlags()
    ff.enable("my_feature")
    assert ff.is_enabled("my_feature") is True


def test_disable_and_check():
    ff = FeatureFlags()
    ff.enable("my_feature")
    ff.disable("my_feature")
    assert ff.is_enabled("my_feature") is False


def test_unknown_flag_is_disabled():
    ff = FeatureFlags()
    assert ff.is_enabled("nonexistent") is False


def test_load_from_config():
    ff = FeatureFlags(config_path=CONFIG_PATH)
    assert ff.is_enabled("new_dashboard") is True
    assert ff.is_enabled("dark_mode") is False


def test_rollout_percentage_deterministic():
    ff = FeatureFlags()
    ff.set_rollout_percentage("beta", 50)
    results = {ff.is_enabled("beta", user_id=f"user_{i}") for i in range(100)}
    assert True in results
    assert False in results


def test_rollout_100_percent():
    ff = FeatureFlags()
    ff.set_rollout_percentage("feature", 100)
    for i in range(20):
        assert ff.is_enabled("feature", user_id=f"user_{i}") is True


def test_rollout_0_percent():
    ff = FeatureFlags()
    ff.set_rollout_percentage("feature", 0)
    for i in range(20):
        assert ff.is_enabled("feature", user_id=f"user_{i}") is False


def test_get_all_flags():
    ff = FeatureFlags()
    ff.enable("a")
    ff.disable("b")
    all_flags = ff.get_all_flags()
    assert "a" in all_flags
    assert "b" in all_flags


def test_app_new_dashboard_gated():
    ff = FeatureFlags()
    ff.enable("new_dashboard")
    assert new_dashboard(ff) == "new dashboard"
    ff.disable("new_dashboard")
    assert new_dashboard(ff) == "classic dashboard"


def test_app_dark_mode_gated():
    ff = FeatureFlags()
    ff.disable("dark_mode")
    assert dark_mode(ff) == "light"
    ff.enable("dark_mode")
    assert dark_mode(ff) == "dark"
