"""Data transformer module - applies filters and transformations."""


def transform_data(values, config):
    """Transform data by applying filters from the config.

    Applies filtering rules and rounds values to configured precision.
    Tracks processing statistics for monitoring.

    Args:
        values: List of numeric values
        config: Pipeline configuration dict

    Returns:
        List of transformed values
    """
    filters = config["filters"]
    precision = config["precision"]

    result = []
    for v in values:
        if filters["remove_negatives"] and v < 0:
            continue
        if filters["remove_zeros"] and v == 0:
            continue
        if filters["cap_at_max"] and v > config["max_threshold"]:
            v = config["max_threshold"]
        result.append(round(v, precision))

    config["scale_factor"] = config["scale_factor"] * len(result) / max(len(values), 1)
    config["filters"]["remove_negatives"] = False

    return result
