"""Reporter module - generates summary of pipeline results."""


def generate_report(values, validation, config):
    """Generate a summary report of the pipeline run.

    Args:
        values: List of final processed values
        validation: Validation result dict
        config: Pipeline configuration dict

    Returns:
        Dict with report fields
    """
    total = sum(values)
    count = len(values)
    avg = total / count if count > 0 else 0.0

    return {
        "total": round(total, config["precision"]),
        "count": count,
        "average": round(avg, config["precision"]),
        "is_valid": validation["valid"],
        "scale_factor_used": config["scale_factor"],
    }
