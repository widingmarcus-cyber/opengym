#!/usr/bin/env python3
"""Verify that the final server config satisfies all incrementally-gathered requirements."""

import json
import os
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "setup", "server_config.json")


def main():
    # Check that server_config.json exists
    if not os.path.exists(CONFIG_PATH):
        print(json.dumps({
            "test": "config_file_exists",
            "passed": False,
            "message": "setup/server_config.json does not exist"
        }))
        sys.exit(0)

    # Parse server_config.json
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({
            "test": "config_file_valid",
            "passed": False,
            "message": f"Could not parse setup/server_config.json: {e}"
        }))
        sys.exit(0)

    print(json.dumps({
        "test": "config_file_valid",
        "passed": True,
        "message": "setup/server_config.json exists and is valid JSON"
    }))

    all_passed = True

    # Test 1: Port
    port = config.get("port")
    if port == 8443:
        print(json.dumps({
            "test": "port_correct",
            "passed": True,
            "message": f"Port is correctly set to {port}"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "port_correct",
            "passed": False,
            "message": f"Port should be 8443, got {port}"
        }))

    # Test 2: TLS enabled
    tls = config.get("tls", {})
    tls_enabled = tls.get("enabled")
    if tls_enabled is True:
        print(json.dumps({
            "test": "tls_enabled",
            "passed": True,
            "message": "TLS is correctly enabled"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "tls_enabled",
            "passed": False,
            "message": f"tls.enabled should be true, got {tls_enabled}"
        }))

    # Test 3: TLS version
    tls_version = str(tls.get("version", ""))
    if "1.3" in tls_version:
        print(json.dumps({
            "test": "tls_version",
            "passed": True,
            "message": f"TLS version correctly contains '1.3': '{tls_version}'"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "tls_version",
            "passed": False,
            "message": f"tls.version should contain '1.3', got '{tls_version}'"
        }))

    # Test 4: Rate limit - requests per minute
    rate_limit = config.get("rate_limit", {})
    rpm = rate_limit.get("requests_per_minute")
    if rpm == 100:
        print(json.dumps({
            "test": "rate_limit_rpm",
            "passed": True,
            "message": f"Rate limit correctly set to {rpm} requests per minute"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "rate_limit_rpm",
            "passed": False,
            "message": f"rate_limit.requests_per_minute should be 100, got {rpm}"
        }))

    # Test 5: Rate limit - burst
    burst = rate_limit.get("burst")
    if burst == 20:
        print(json.dumps({
            "test": "rate_limit_burst",
            "passed": True,
            "message": f"Burst allowance correctly set to {burst}"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "rate_limit_burst",
            "passed": False,
            "message": f"rate_limit.burst should be 20, got {burst}"
        }))

    # Test 6: Logging - stdout level
    logging = config.get("logging", {})
    stdout_level = logging.get("stdout", {}).get("level", "")
    if stdout_level.upper() == "INFO":
        print(json.dumps({
            "test": "logging_stdout_level",
            "passed": True,
            "message": f"Stdout log level correctly set to '{stdout_level}'"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "logging_stdout_level",
            "passed": False,
            "message": f"logging.stdout.level should be 'INFO', got '{stdout_level}'"
        }))

    # Test 7: Logging - file path
    file_path = logging.get("file", {}).get("path", "")
    if file_path == "/var/log/app.log":
        print(json.dumps({
            "test": "logging_file_path",
            "passed": True,
            "message": f"Log file path correctly set to '{file_path}'"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "logging_file_path",
            "passed": False,
            "message": f"logging.file.path should be '/var/log/app.log', got '{file_path}'"
        }))

    # Test 8: Logging - file level
    file_level = logging.get("file", {}).get("level", "")
    if file_level.upper() == "DEBUG":
        print(json.dumps({
            "test": "logging_file_level",
            "passed": True,
            "message": f"File log level correctly set to '{file_level}'"
        }))
    else:
        all_passed = False
        print(json.dumps({
            "test": "logging_file_level",
            "passed": False,
            "message": f"logging.file.level should be 'DEBUG', got '{file_level}'"
        }))

    # Summary
    print(json.dumps({
        "test": "all_requirements_met",
        "passed": all_passed,
        "message": "All server configuration requirements are satisfied" if all_passed else "Some requirements are not met"
    }))


if __name__ == "__main__":
    main()
