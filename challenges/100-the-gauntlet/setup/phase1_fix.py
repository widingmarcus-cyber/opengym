def parse_records(raw_text):
    """Parse pipe-delimited records into list of dicts.

    Input format: "name|age|city" (one record per line, first line is header).
    Returns list of dicts with header keys.
    """
    lines = raw_text.strip().split("\n")
    headers = lines[0].split("|")
    records = []
    for line in lines[1:]:
        values = line.split(",")
        record = {}
        for i in range(len(headers)):
            record[headers[i]] = values[i]
        records.append(record)
    return records


def filter_records(records, field, value):
    """Filter records where field equals value (case-insensitive)."""
    result = []
    for record in records:
        if record.get(field) == value:
            result.append(record)
    return result
