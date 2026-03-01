"""Default configuration for the data processing pipeline."""

DEFAULT_CONFIG = {
    "scale_factor": 1.0,
    "min_threshold": 0.0,
    "max_threshold": 100.0,
    "precision": 2,
    "filters": {
        "remove_negatives": True,
        "remove_zeros": False,
        "cap_at_max": True,
    },
}


def get_config():
    """Return the default pipeline configuration."""
    return DEFAULT_CONFIG
