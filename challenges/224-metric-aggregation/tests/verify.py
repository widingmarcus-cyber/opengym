import json
import os
import csv
import math

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_csv():
    path = os.path.join(CHALLENGE_DIR, "setup", "metrics.csv")
    metrics = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["metric_name"]
            val = float(row["value"])
            metrics.setdefault(name, []).append(val)
    return metrics


def _percentile_nearest_rank(sorted_values, p):
    """Nearest-rank percentile."""
    n = len(sorted_values)
    rank = math.ceil(p / 100.0 * n)
    return sorted_values[min(rank - 1, n - 1)]


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "summary.json not found in setup/"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(json.dumps({"test": "output_exists", "passed": False, "message": "summary.json must contain a JSON object"}))
            return False
        print(json.dumps({"test": "output_exists", "passed": True, "message": "summary.json exists and is valid JSON"}))
        return True
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "output_exists", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return False


def test_all_metrics_present():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_metrics_present", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    expected = {"cpu_usage", "memory_mb", "request_latency_ms"}
    actual = set(data.keys())
    if expected != actual:
        missing = expected - actual
        extra = actual - expected
        msg = ""
        if missing:
            msg += f"Missing: {sorted(missing)}. "
        if extra:
            msg += f"Unexpected: {sorted(extra)}."
        print(json.dumps({"test": "all_metrics_present", "passed": False, "message": msg.strip()}))
        return
    print(json.dumps({"test": "all_metrics_present", "passed": True, "message": "All 3 metrics present"}))


def test_required_stats_fields():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "required_stats_fields", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    required = {"count", "min", "max", "avg", "p50", "p95", "p99"}
    for metric_name, stats in data.items():
        missing = required - set(stats.keys())
        if missing:
            print(json.dumps({"test": "required_stats_fields", "passed": False, "message": f"Metric '{metric_name}' missing fields: {sorted(missing)}"}))
            return
    print(json.dumps({"test": "required_stats_fields", "passed": True, "message": "All metrics have required stat fields"}))


def test_counts_correct():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "counts_correct", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    raw = _load_csv()
    for metric_name, values in raw.items():
        expected_count = len(values)
        actual_count = data.get(metric_name, {}).get("count", -1)
        if actual_count != expected_count:
            print(json.dumps({"test": "counts_correct", "passed": False, "message": f"Metric '{metric_name}' count: expected {expected_count}, got {actual_count}"}))
            return
    print(json.dumps({"test": "counts_correct", "passed": True, "message": "All counts correct (20 per metric)"}))


def test_calculations_accurate():
    path = os.path.join(CHALLENGE_DIR, "setup", "summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "calculations_accurate", "passed": False, "message": "summary.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    raw = _load_csv()
    tolerance = 0.05  # Allow small rounding differences
    for metric_name, values in raw.items():
        sorted_vals = sorted(values)
        expected_min = round(min(values), 2)
        expected_max = round(max(values), 2)
        expected_avg = round(sum(values) / len(values), 2)
        expected_p95 = round(_percentile_nearest_rank(sorted_vals, 95), 2)

        stats = data.get(metric_name, {})
        checks = [
            ("min", expected_min, stats.get("min")),
            ("max", expected_max, stats.get("max")),
            ("avg", expected_avg, stats.get("avg")),
            ("p95", expected_p95, stats.get("p95")),
        ]
        for field, expected, actual in checks:
            if actual is None:
                print(json.dumps({"test": "calculations_accurate", "passed": False, "message": f"Metric '{metric_name}' missing '{field}'"}))
                return
            if abs(float(actual) - expected) > tolerance:
                print(json.dumps({"test": "calculations_accurate", "passed": False, "message": f"Metric '{metric_name}' {field}: expected {expected}, got {actual}"}))
                return
    print(json.dumps({"test": "calculations_accurate", "passed": True, "message": "All min/max/avg/p95 calculations are accurate"}))


if __name__ == "__main__":
    test_output_exists()
    test_all_metrics_present()
    test_required_stats_fields()
    test_counts_correct()
    test_calculations_accurate()
