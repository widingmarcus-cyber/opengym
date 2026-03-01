import math
import yaml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def process_amounts(amounts):
    """Process financial amounts according to config."""
    config = load_config()
    precision = config["processing"]["precision"]
    rounding = config["processing"]["rounding"]

    results = []
    for amount in amounts:
        if rounding == "round":
            processed = round(amount, precision)
        elif rounding == "floor":
            factor = 10 ** precision
            processed = math.floor(amount * factor) / factor
        elif rounding == "ceil":
            factor = 10 ** precision
            processed = math.ceil(amount * factor) / factor
        else:
            processed = round(amount, precision)
        results.append(processed)
    return results

def calculate_total(amounts):
    """Calculate total of processed amounts."""
    processed = process_amounts(amounts)
    return sum(processed)
