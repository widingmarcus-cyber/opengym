#!/usr/bin/env python3
"""Verify Challenge 121: Shared Config — both agents wrote their sections without overwriting."""

import json
import os
import sys
import yaml

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(CHALLENGE_DIR, "setup", "shared_config.yaml")

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def main():
    # Load the config file
    if not os.path.exists(CONFIG_PATH):
        check("config_exists", False, f"shared_config.yaml not found at {CONFIG_PATH}")
        print_results()
        return

    with open(CONFIG_PATH, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            check("config_parse", False, f"Failed to parse YAML: {e}")
            print_results()
            return

    if not isinstance(config, dict):
        check("config_is_dict", False, "Config file did not parse to a dictionary")
        print_results()
        return

    # Check database section
    db = config.get("database")
    check(
        "database_section_exists",
        db is not None and isinstance(db, dict),
        "database section must exist as a mapping",
    )

    if isinstance(db, dict):
        check(
            "database_host",
            db.get("host") == "db.internal.company.com",
            f"Expected host 'db.internal.company.com', got '{db.get('host')}'",
        )
        check(
            "database_port",
            db.get("port") == 5432,
            f"Expected port 5432, got {db.get('port')}",
        )
        check(
            "database_pool_size",
            db.get("pool_size") == 20,
            f"Expected pool_size 20, got {db.get('pool_size')}",
        )
    else:
        check("database_host", False, "database section missing")
        check("database_port", False, "database section missing")
        check("database_pool_size", False, "database section missing")

    # Check cache section
    cache = config.get("cache")
    check(
        "cache_section_exists",
        cache is not None and isinstance(cache, dict),
        "cache section must exist as a mapping",
    )

    if isinstance(cache, dict):
        check(
            "cache_provider",
            cache.get("provider") == "redis",
            f"Expected provider 'redis', got '{cache.get('provider')}'",
        )
        check(
            "cache_host",
            cache.get("host") == "cache.internal.company.com",
            f"Expected host 'cache.internal.company.com', got '{cache.get('host')}'",
        )
        check(
            "cache_ttl",
            cache.get("ttl") == 3600,
            f"Expected ttl 3600, got {cache.get('ttl')}",
        )
    else:
        check("cache_provider", False, "cache section missing")
        check("cache_host", False, "cache section missing")
        check("cache_ttl", False, "cache section missing")

    # Check coexistence — both sections must be present
    both_exist = (
        isinstance(config.get("database"), dict) and isinstance(config.get("cache"), dict)
    )
    check(
        "both_sections_coexist",
        both_exist,
        "Both database and cache sections must coexist (neither agent should overwrite the other)",
    )

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
