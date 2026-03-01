import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from parser import parse_csv
from formatter import format_table
from reporter import generate_report


def test_parse_simple():
    csv = "name,age\nAlice,30\nBob,25"
    result = parse_csv(csv)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == "30"
    assert result[1]["name"] == "Bob"


def test_parse_quoted():
    csv = 'name,title\nAlice,"Manager, Sales"\nBob,"Director, Ops"'
    result = parse_csv(csv)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["title"] == "Manager, Sales"
    assert result[1]["title"] == "Director, Ops"


def test_format_table():
    records = [
        {"name": "Alice", "role": "Engineer"},
        {"name": "Bob", "role": "Manager"},
    ]
    table = format_table(records)
    lines = table.split("\n")
    # Header line should exist
    assert "name" in lines[0]
    assert "role" in lines[0]
    # Separator line
    assert set(lines[1].replace(" ", "")) <= {"-", "|"}
    # Data lines should be aligned with headers
    # Each column should be wide enough to fit the longest value
    assert "Alice" in lines[2]
    assert "Engineer" in lines[2]
    assert "Bob" in lines[3]
    assert "Manager" in lines[3]
    # Columns should be properly aligned (same width)
    header_parts = lines[0].split(" | ")
    row1_parts = lines[2].split(" | ")
    for hp, rp in zip(header_parts, row1_parts):
        assert len(hp) == len(rp), f"Column widths don't match: '{hp}' vs '{rp}'"


def test_format_empty():
    assert format_table([]) == ""


def test_report_basic():
    csv = "product,price\nWidget,9.99\nGadget,24.99"
    report = generate_report(csv, title="Inventory")
    assert "=== Inventory ===" in report
    assert "Widget" in report
    assert "Gadget" in report
    assert "=== End ===" in report


def test_report_empty():
    # Empty CSV (no data rows, just headers or empty string) should not crash
    report = generate_report("name,age", title="Empty")
    assert "=== Empty ===" in report
    assert "=== End ===" in report


def test_report_quoted_values():
    csv = 'name,address\nAlice,"123 Main St, Apt 4"\nBob,"456 Oak Ave, Suite 7"'
    report = generate_report(csv, title="Addresses")
    assert "=== Addresses ===" in report
    assert "123 Main St, Apt 4" in report
    assert "456 Oak Ave, Suite 7" in report
    assert "=== End ===" in report


def test_parse_quoted_commas_in_values():
    """CSV with values containing commas inside quotes must parse correctly."""
    csv = 'name,title\nAlice,"Lead, Engineering"'
    result = parse_csv(csv)
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
    assert result[0]["title"] == "Lead, Engineering"


def test_format_table_column_alignment_long_values():
    """Columns must be wide enough to fit values longer than headers."""
    records = [
        {"id": "1", "description": "A very long description here"},
        {"id": "2", "description": "Short"},
    ]
    table = format_table(records)
    lines = table.split("\n")
    header_parts = lines[0].split(" | ")
    row1_parts = lines[2].split(" | ")
    row2_parts = lines[3].split(" | ")
    # Every column in every row must have equal width
    for hp, rp in zip(header_parts, row1_parts):
        assert len(hp) == len(rp), f"Column widths don't match: header '{hp}' vs row '{rp}'"
    for hp, rp in zip(header_parts, row2_parts):
        assert len(hp) == len(rp), f"Column widths don't match: header '{hp}' vs row '{rp}'"
    # The description column must be wide enough for the longest value
    desc_col_idx = [i for i, h in enumerate(header_parts) if h.strip() == "description"][0]
    assert "A very long description here" in row1_parts[desc_col_idx]


def test_parse_field_count_matches_headers():
    """Each parsed record must have exactly as many fields as there are headers."""
    csv = 'name,title,dept\nAlice,"Lead, Engineering",Sales'
    result = parse_csv(csv)
    assert len(result) == 1
    assert len(result[0]) == 3
    assert result[0]["name"] == "Alice"
    assert result[0]["title"] == "Lead, Engineering"
    assert result[0]["dept"] == "Sales"
