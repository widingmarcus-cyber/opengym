"""Operation log replayer — BUG: non-deterministic due to unseeded RNG and timestamps.
Fix this to produce deterministic replay by using the seed and fixed_timestamp from each log entry."""

import json
import random
import os
from datetime import datetime

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

def replay(log_path, output_path):
    with open(log_path) as f:
        log = json.load(f)

    state = []
    results = []

    for entry in log:
        op = entry["op"]
        params = entry["params"]
        # BUG: should use entry["seed"] to seed RNG, but doesn't
        # BUG: uses current timestamp instead of entry["fixed_timestamp"]

        if op == "init":
            state = list(params["values"])
            results.append({"seq": entry["seq"], "op": op, "state": list(state), "timestamp": datetime.now().isoformat()})

        elif op == "shuffle":
            # BUG: random shuffle without seeding — different each run
            random.shuffle(state)
            results.append({"seq": entry["seq"], "op": op, "state": list(state), "timestamp": datetime.now().isoformat()})

        elif op == "add_noise":
            noise_range = params["noise_range"]
            # BUG: random noise without seeding
            state = [v + random.randint(-noise_range, noise_range) for v in state]
            results.append({"seq": entry["seq"], "op": op, "state": list(state), "timestamp": datetime.now().isoformat()})

        elif op == "sample":
            count = params["count"]
            # BUG: random sample without seeding
            state = random.sample(state, count)
            results.append({"seq": entry["seq"], "op": op, "state": list(state), "timestamp": datetime.now().isoformat()})

        elif op == "finalize":
            state = sorted(state)
            results.append({"seq": entry["seq"], "op": op, "state": list(state), "timestamp": datetime.now().isoformat()})

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    replay(
        os.path.join(SETUP_DIR, "operation_log.json"),
        os.path.join(SETUP_DIR, "replay_output.json")
    )
