"""Data validator module - checks that values meet config thresholds."""


def validate_data(values, config):
    """Validate that all values are within configured thresholds.

    Args:
        values: List of numeric values
        config: Pipeline configuration dict

    Returns:
        Dict with 'valid' (bool), 'count' (int), 'out_of_range' (list)
    """
    min_t = config["min_threshold"]
    max_t = config["max_threshold"]

    out_of_range = []
    for v in values:
        if v < min_t or v > max_t:
            out_of_range.append(v)

    return {
        "valid": len(out_of_range) == 0,
        "count": len(values),
        "out_of_range": out_of_range,
    }
