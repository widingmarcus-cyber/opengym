"""Data processing pipeline for batch record transformation."""


def log_error(error):
    """Log an error message."""
    print(f"Error: {error}")


def parse_metadata(record):
    """Parse metadata from a record.

    Returns a dict with parsed metadata fields, or None if
    the metadata field is missing from the record.
    """
    raw = record.get("metadata")
    if raw is None:
        return None
    parts = raw.split(";")
    result = {}
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def clean_data(data):
    """Clean and normalize data dictionary.

    Strips whitespace from all string values and lowercases keys.
    """
    cleaned = {}
    for key in data.keys():
        value = data[key]
        if isinstance(value, str):
            value = value.strip()
        cleaned[key.lower()] = value
    return cleaned


def transform_record(record):
    """Transform a single record through the processing pipeline."""
    raw_data = parse_metadata(record)
    cleaned = clean_data(raw_data)
    cleaned["processed"] = True
    return cleaned


def enrich_record(cleaned_record):
    """Add derived fields to a cleaned record."""
    if "timestamp" in cleaned_record:
        cleaned_record["date"] = cleaned_record["timestamp"][:10]
    if "value" in cleaned_record:
        try:
            cleaned_record["value_numeric"] = float(cleaned_record["value"])
        except (ValueError, TypeError):
            cleaned_record["value_numeric"] = 0.0
    return cleaned_record


def process_batch(batch):
    """Process a batch of records."""
    results = []
    for record in batch:
        transformed = transform_record(record)
        enriched = enrich_record(transformed)
        results.append(enriched)
    return results


def validate_batch(batch):
    """Check that a batch has at least one record."""
    if not batch:
        raise ValueError("Empty batch")
    return True


def run_pipeline():
    """Run the full data processing pipeline."""
    batch = fetch_batch()
    validate_batch(batch)
    try:
        results = process_batch(batch)
    except Exception as e:
        log_error(e)
        raise
    return results


def main():
    """Entry point."""
    try:
        run_pipeline()
    except Exception as e:
        log_error(e)


def fetch_batch():
    """Fetch a batch of records from the data source."""
    return [
        {"id": 1, "metadata": "name=Alice;timestamp=2025-01-01 00:00:00;value=42.5"},
        {"id": 2, "metadata": "name=Bob;timestamp=2025-01-02 12:00:00;value=17.3"},
        {"id": 3},
    ]
