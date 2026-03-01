"""Tests for Challenge 057: Parse Changelog."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    latest_version,
    total_releases,
    breaking_changes_count,
    first_release_date,
    features_in_version,
    versions_with_breaking_changes,
)


def test_latest_version():
    assert latest_version() == "2.5.0"


def test_total_releases():
    assert total_releases() == 20


def test_breaking_changes_count():
    assert breaking_changes_count() == 10


def test_first_release_date():
    assert first_release_date() == "2022-01-15"


def test_features_in_latest_version():
    features = features_in_version("2.5.0")
    assert len(features) == 3
    assert "Added WebSocket support for real-time notifications" in features


def test_features_in_initial_release():
    features = features_in_version("1.0.0")
    assert len(features) == 5
    assert "Initial public release" in features


def test_versions_with_breaking_changes():
    result = versions_with_breaking_changes()
    expected = ["1.2.0", "1.5.0", "1.7.0", "2.0.0", "2.2.0", "2.4.0"]
    assert result == expected


def test_features_in_version_with_breaking():
    features = features_in_version("2.0.0")
    assert len(features) == 3
    assert "Complete API redesign with versioned endpoints" in features
    for f in features:
        assert "Migrated" not in f
