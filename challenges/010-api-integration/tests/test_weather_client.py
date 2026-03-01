"""Tests for Challenge 010: API Client Integration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from weather_client import (
    get_current_weather,
    get_forecast,
    get_coldest_city,
    will_it_rain,
    format_report,
)


# --- get_current_weather ---

def test_current_weather_valid():
    result = get_current_weather("London")
    assert result is not None
    assert result["city"] == "London"
    assert result["temperature"] == 12
    assert result["condition"] == "cloudy"


def test_current_weather_case_insensitive():
    result = get_current_weather("london")
    assert result is not None
    assert result["city"] == "London"


def test_current_weather_invalid_city():
    result = get_current_weather("Atlantis")
    assert result is None


# --- get_forecast ---

def test_forecast_default_3_days():
    result = get_forecast("Paris")
    assert isinstance(result, list)
    assert len(result) == 3


def test_forecast_custom_days():
    result = get_forecast("Tokyo", days=5)
    assert len(result) == 5


def test_forecast_max_7_days():
    result = get_forecast("London", days=7)
    assert len(result) == 7


def test_forecast_has_day_numbers():
    result = get_forecast("Berlin", days=3)
    assert result[0]["day"] == 1
    assert result[1]["day"] == 2
    assert result[2]["day"] == 3


def test_forecast_invalid_city():
    result = get_forecast("Atlantis")
    assert result == [] or result is None


# --- get_coldest_city ---

def test_coldest_city():
    # Berlin=5, London=12, Cairo=35
    result = get_coldest_city(["London", "Berlin", "Cairo"])
    assert result == "Berlin"


def test_coldest_city_two():
    # New York=8, Mumbai=33
    result = get_coldest_city(["New York", "Mumbai"])
    assert result == "New York"


# --- will_it_rain ---

def test_will_it_rain_london():
    # London forecast has rainy days
    assert will_it_rain("London") is True


def test_will_it_rain_cairo():
    # Cairo forecast is all sunny
    assert will_it_rain("Cairo", days=7) is False


def test_will_it_rain_tokyo():
    # Tokyo forecast has rainy days
    assert will_it_rain("Tokyo") is True


# --- format_report ---

def test_format_report_contains_city():
    report = format_report("London")
    assert "London" in report


def test_format_report_contains_temperature():
    report = format_report("London")
    assert "12" in report


def test_format_report_contains_condition():
    report = format_report("London")
    assert "cloudy" in report.lower() or "Cloudy" in report


def test_format_report_is_multiline():
    report = format_report("London")
    lines = report.strip().split("\n")
    assert len(lines) >= 3, "Report should be at least 3 lines"


def test_format_report_contains_forecast():
    report = format_report("Paris")
    # Should mention forecast data
    assert "forecast" in report.lower() or "day" in report.lower()
