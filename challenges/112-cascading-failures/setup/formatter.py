def format_table(records):
    """Format records as a text table."""
    if not records:
        return ""
    headers = list(records[0].keys())
    # BUG: uses len(headers[0]) instead of max value length for column width
    col_width = len(headers[0])  # Should compute max width per column

    lines = []
    header_line = " | ".join(h.ljust(col_width) for h in headers)
    lines.append(header_line)
    lines.append("-" * len(header_line))
    for record in records:
        line = " | ".join(str(record[h]).ljust(col_width) for h in headers)
        lines.append(line)
    return "\n".join(lines)
