import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import yaml
from phase1_fix import filter_records, parse_records
from phase2_implement import summarize_records
from phase3_refactor import process_employees
from phase5_integrate import run_pipeline


# ---------------------------------------------------------------------------
# Phase 1: Fix
# ---------------------------------------------------------------------------

def test_parse_records_basic():
    raw = "name|age\nAlice|30\nBob|25"
    result = parse_records(raw)
    assert len(result) == 2
    assert result[0] == {"name": "Alice", "age": "30"}
    assert result[1] == {"name": "Bob", "age": "25"}


def test_parse_records_multiline():
    raw = textwrap.dedent("""\
        name|age|city
        Alice|30|NYC
        Bob|25|LA
        Carol|35|NYC
        Dave|28|Chicago
        Eve|40|LA""")
    result = parse_records(raw)
    assert len(result) == 5
    assert result[0]["city"] == "NYC"
    assert result[4]["name"] == "Eve"


def test_filter_case_insensitive():
    records = [
        {"name": "Alice", "city": "NYC"},
        {"name": "Bob", "city": "nyc"},
        {"name": "Carol", "city": "Nyc"},
        {"name": "Dave", "city": "LA"},
    ]
    result = filter_records(records, "city", "NYC")
    assert len(result) == 3
    names = [r["name"] for r in result]
    assert "Alice" in names
    assert "Bob" in names
    assert "Carol" in names


# ---------------------------------------------------------------------------
# Phase 2: Implement
# ---------------------------------------------------------------------------

def test_summarize_basic():
    records = [
        {"city": "NYC", "dept": "Sales"},
        {"city": "NYC", "dept": "HR"},
        {"city": "NYC", "dept": "Sales"},
        {"city": "LA", "dept": "Sales"},
    ]
    result = summarize_records(records, "city", "dept")
    assert result == {"NYC": 2, "LA": 1}


def test_summarize_empty():
    result = summarize_records([], "city", "dept")
    assert result == {}


# ---------------------------------------------------------------------------
# Phase 3: Refactor
# ---------------------------------------------------------------------------

def test_refactor_still_works():
    employees = [
        {"name": "Alice", "department": "Engineering", "salary": 100000, "years": 6},
        {"name": "Bob", "department": "Engineering", "salary": 90000, "years": 3},
        {"name": "Carol", "department": "Sales", "salary": 80000, "years": 7},
        {"name": "Dave", "department": "Sales", "salary": 70000, "years": 2},
        {"name": "Eve", "department": "Engineering", "salary": 110000, "years": 10},
    ]
    result = process_employees(employees)

    eng = result["Engineering"]
    assert eng["count"] == 3
    assert eng["total_salary"] == 300000
    assert eng["avg_salary"] == 100000.0
    assert eng["senior_count"] == 2
    assert eng["junior_count"] == 1

    sales = result["Sales"]
    assert sales["count"] == 2
    assert sales["total_salary"] == 150000
    assert sales["avg_salary"] == 75000.0
    assert sales["senior_count"] == 1
    assert sales["junior_count"] == 1


def test_refactor_code_quality():
    source_path = Path(__file__).parent.parent / "setup" / "phase3_refactor.py"
    source = source_path.read_text()

    assert "+=" in source, "Refactored code should use the += operator instead of x = x + y"

    repetitive_pattern = 'result[dept]["'
    occurrences = source.count(repetitive_pattern)
    assert occurrences < 12, (
        f"Code still has too many repetitive 'result[dept][\"...\"]' patterns "
        f"({occurrences} found). Refactor to reduce duplication."
    )


# ---------------------------------------------------------------------------
# Phase 4: Configure
# ---------------------------------------------------------------------------

def test_config_port_is_integer():
    config_path = Path(__file__).parent.parent / "setup" / "phase4_config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    port = config["database"]["port"]
    assert isinstance(port, int), f"port should be an integer, got {type(port).__name__}: {port}"
    assert port == 5000


def test_config_max_records_positive():
    config_path = Path(__file__).parent.parent / "setup" / "phase4_config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    max_records = config["limits"]["max_records"]
    assert isinstance(max_records, int), f"max_records should be an integer, got {type(max_records).__name__}"
    assert max_records > 0, f"max_records should be positive, got {max_records}"
    assert max_records == 100


# ---------------------------------------------------------------------------
# Phase 5: Integrate
# ---------------------------------------------------------------------------

def test_pipeline_no_filter():
    raw = "name|city|dept\nAlice|NYC|Sales\nBob|LA|HR\nCarol|NYC|HR"
    config_path = str(Path(__file__).parent.parent / "setup" / "phase4_config.yaml")
    result = run_pipeline(raw, config_path, "city", "dept")

    assert "config" in result
    assert "record_count" in result
    assert "summary" in result
    assert "enabled_features" in result
    assert result["record_count"] == 3
    assert result["summary"] == {"NYC": 2, "LA": 1}


def test_pipeline_with_filter():
    raw = "name|city|dept\nAlice|NYC|Sales\nBob|LA|HR\nCarol|NYC|HR\nDave|nyc|Sales"
    config_path = str(Path(__file__).parent.parent / "setup" / "phase4_config.yaml")
    result = run_pipeline(raw, config_path, "city", "dept", filter_field="city", filter_value="NYC")

    assert result["record_count"] == 3
    assert "NYC" in result["summary"] or "nyc" in result["summary"]


def test_pipeline_enabled_features():
    raw = "name|city\nAlice|NYC"
    config_path = str(Path(__file__).parent.parent / "setup" / "phase4_config.yaml")
    result = run_pipeline(raw, config_path, "city", "name")

    assert sorted(result["enabled_features"]) == ["caching", "logging"]
