"""Long-running worker — has no graceful shutdown handling.
If killed, all progress is lost. Fix this."""

import json
import time
import os

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

def process_task(task):
    """Process a single task: result = a * b + c"""
    result = task["a"] * task["b"] + task["c"]
    return {**task, "result": result}

def run():
    with open(os.path.join(SETUP_DIR, "task_queue.json")) as f:
        tasks = json.load(f)

    # No handling for termination — if killed, all progress is lost
    results = []
    for task in tasks:
        result = process_task(task)
        results.append(result)
        time.sleep(0.1)  # simulate work

    # Only reached if never interrupted — no partial save
    with open(os.path.join(SETUP_DIR, "completed.json"), "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
