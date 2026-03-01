"""Data processing pipeline with validate, transform, and aggregate stages."""


def validate(records):
    """Filter records, keeping only those with 'name' and 'amount' keys.

    Args:
        records: list of dicts

    Returns:
        list of dicts that have both 'name' and 'amount' keys

    Raises:
        TypeError: if records is not a list
    """
    try:
        valid = []
        for record in records:
            if "name" in record and "amount" in record:
                valid.append(record)
        return valid
    except:
        return []


def transform(records):
    """Transform each record: uppercase name, convert amount to float, add 'processed' flag.

    Args:
        records: list of dicts with 'name' and 'amount'

    Returns:
        list of transformed dicts

    Raises:
        ValueError: if an amount value cannot be converted to float
    """
    try:
        result = []
        for record in records:
            new_record = {
                "name": record["name"].upper(),
                "amount": float(record["amount"]),
                "processed": True,
            }
            result.append(new_record)
        return result
    except:
        return []


def aggregate(records):
    """Aggregate records into a summary.

    Args:
        records: list of dicts with 'name', 'amount', 'processed'

    Returns:
        dict with 'total_amount' (float), 'count' (int), 'names' (list of str)

    Raises:
        TypeError: if records is not a list
    """
    try:
        total = 0.0
        names = []
        for record in records:
            total += record["amount"]
            names.append(record["name"])
        return {
            "total_amount": total,
            "count": len(records),
            "names": names,
        }
    except:
        return {"total_amount": 0.0, "count": 0, "names": []}


def process_records(records):
    """Run the full pipeline: validate -> transform -> aggregate.

    Args:
        records: list of dicts

    Returns:
        dict: aggregated summary
    """
    try:
        validated = validate(records)
        transformed = transform(validated)
        return aggregate(transformed)
    except:
        return {"total_amount": 0.0, "count": 0, "names": []}
