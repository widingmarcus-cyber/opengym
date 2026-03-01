"""Data loader module - reads raw data and applies initial config."""


def load_data(raw_values, config):
    """Load raw data values and apply the configured scale factor.

    Args:
        raw_values: List of numeric values
        config: Pipeline configuration dict

    Returns:
        List of scaled values
    """
    scale = config["scale_factor"]
    return [v * scale for v in raw_values]
