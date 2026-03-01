#!/usr/bin/env python3
"""City population lookup tool with rate limiting.

Enforces a maximum of 3 calls per 10-second window using a persistent
state file at tools/.state/rate_limit.json.
"""

import json
import os
import sys
import time
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(SCRIPT_DIR, ".state")
RATE_FILE = os.path.join(STATE_DIR, "rate_limit.json")

MAX_CALLS = 3
WINDOW_SECONDS = 10

# Population data (approximate, in thousands rounded)
CITIES = {
    "Stockholm": 975000,
    "Gothenburg": 583000,
    "Malmö": 347000,
    "Uppsala": 233000,
    "Linköping": 164000,
    "Västerås": 155000,
    "Örebro": 157000,
    "Helsingborg": 149000,
    "Norrköping": 143000,
    "Jönköping": 144000,
}


def load_timestamps():
    """Load the list of call timestamps from state file."""
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(RATE_FILE):
        return []
    try:
        with open(RATE_FILE, "r") as f:
            timestamps = json.load(f)
        if not isinstance(timestamps, list):
            return []
        return [float(t) for t in timestamps]
    except (json.JSONDecodeError, ValueError, IOError):
        return []


def save_timestamps(timestamps):
    """Save the list of call timestamps to state file."""
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(RATE_FILE, "w") as f:
        json.dump(timestamps, f)


def main():
    # Ensure consistent UTF-8 output across platforms
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Look up population for a Swedish city.")
        print("Usage: python lookup.py CITY_NAME")
        print()
        print("Returns JSON with city name and population.")
        print("Rate limit: 3 requests per 10 seconds.")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Error: No city name provided. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    city = unicodedata.normalize("NFC", sys.argv[1].strip())
    now = time.time()

    # Load existing timestamps and prune old ones
    timestamps = load_timestamps()
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    # Check rate limit
    if len(timestamps) >= MAX_CALLS:
        oldest = min(timestamps)
        wait_time = WINDOW_SECONDS - (now - oldest)
        print(
            f"Error: Rate limit exceeded. Max {MAX_CALLS} requests per {WINDOW_SECONDS} seconds. "
            f"Try again in {wait_time:.1f}s.",
            file=sys.stderr,
        )
        # Save back the pruned timestamps (don't add this failed call)
        save_timestamps(timestamps)
        sys.exit(2)

    # Record this call
    timestamps.append(now)
    save_timestamps(timestamps)

    # Look up the city
    if city not in CITIES:
        print(f"Error: Unknown city '{city}'", file=sys.stderr)
        sys.exit(1)

    result = {"city": city, "population": CITIES[city]}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
