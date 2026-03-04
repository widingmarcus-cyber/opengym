def parse_csv(text):
    """Parse CSV text into list of dicts."""
    lines = text.strip().split("\n")
    headers = lines[0].split(",")
    records = []
    for line in lines[1:]:
        values = line.split(",")

        records.append(dict(zip(headers, values)))
    return records
