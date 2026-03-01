"""Data processing pipeline using callback-based architecture."""

import hashlib
import time


def fetch_data_cb(url, callback):
    """Fetch data from a URL and pass it to callback."""
    seed = int(hashlib.md5(url.encode()).hexdigest()[:8], 16)
    data = [(seed * (i + 1) * 7 + 13) % 1000 for i in range(20)]
    result = {
        "url": url,
        "data": data,
        "status": "ok",
    }
    callback(result)


def process_data_cb(data, callback):
    """Process a list of numbers and pass results to callback."""
    filtered = [x for x in data if x > 100]
    transformed = [round(x * 1.15 + 10, 2) for x in filtered]
    total = round(sum(transformed), 2)
    count = len(transformed)
    result = {
        "filtered": filtered,
        "transformed": transformed,
        "total": total,
        "count": count,
    }
    callback(result)


def save_results_cb(results, callback):
    """Save processed results and pass confirmation to callback."""
    record_count = results["count"]
    content = f"{results['total']}:{record_count}"
    timestamp = "2025-01-15T10:30:00Z"
    confirmation = {
        "saved": True,
        "record_count": record_count,
        "timestamp": timestamp,
    }
    callback(confirmation)


def run_pipeline_cb(url, final_callback):
    """Run the full pipeline using nested callbacks."""
    def on_fetch(fetch_result):
        def on_process(process_result):
            def on_save(save_result):
                final_callback(save_result)
            save_results_cb(process_result, on_save)
        process_data_cb(fetch_result["data"], on_process)
    fetch_data_cb(url, on_fetch)
