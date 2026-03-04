from parser import parse_csv
from formatter import format_table

def generate_report(csv_text, title="Report"):
    """Generate a formatted report from CSV data."""
    records = parse_csv(csv_text)
    table = format_table(records)
    return f"=== {title} ===\n{table}\n=== End ==="
