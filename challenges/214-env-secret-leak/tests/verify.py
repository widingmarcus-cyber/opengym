import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

# Set known secret values in the environment so we can check for leaks
os.environ["DATABASE_PASSWORD"] = "s3cret_db_pass"
os.environ["API_SECRET_KEY"] = "sk-abc123secret"
os.environ["AWS_SECRET_ACCESS_KEY"] = "AKIASECRETKEY999"
os.environ["APP_NAME"] = "myapp"
os.environ["APP_ENV"] = "production"
os.environ["DEBUG"] = "false"

from app import get_config, log_startup_info, get_debug_dump

SECRETS = ["s3cret_db_pass", "sk-abc123secret", "AKIASECRETKEY999"]


def test_get_config_no_secrets():
    """get_config() must not return plain-text secret values."""
    config = get_config()
    for secret in SECRETS:
        if secret in str(config.values()):
            print(json.dumps({"test": "get_config_no_secrets", "passed": False,
                              "message": f"Secret '{secret}' found in get_config() output"}))
            return
    print(json.dumps({"test": "get_config_no_secrets", "passed": True, "message": "OK"}))


def test_get_config_has_nonsecrets():
    """get_config() must still return non-secret values."""
    config = get_config()
    if config.get("APP_NAME") != "myapp" or config.get("APP_ENV") != "production":
        print(json.dumps({"test": "get_config_has_nonsecrets", "passed": False,
                          "message": f"Non-secret config values are missing or wrong: {config}"}))
        return
    print(json.dumps({"test": "get_config_has_nonsecrets", "passed": True, "message": "OK"}))


def test_log_output_no_secrets():
    """log_startup_info() output must not contain plain-text secrets."""
    log_output = log_startup_info()
    for secret in SECRETS:
        if secret in log_output:
            print(json.dumps({"test": "log_output_no_secrets", "passed": False,
                              "message": f"Secret '{secret}' found in log output"}))
            return
    print(json.dumps({"test": "log_output_no_secrets", "passed": True, "message": "OK"}))


def test_debug_dump_no_secrets():
    """get_debug_dump() must not contain plain-text secrets."""
    dump = get_debug_dump()
    for secret in SECRETS:
        if secret in dump:
            print(json.dumps({"test": "debug_dump_no_secrets", "passed": False,
                              "message": f"Secret '{secret}' found in debug dump"}))
            return
    print(json.dumps({"test": "debug_dump_no_secrets", "passed": True, "message": "OK"}))


def test_redacted_placeholder_present():
    """Secret fields must contain a redaction placeholder."""
    config = get_config()
    for key in ["DATABASE_PASSWORD", "API_SECRET_KEY", "AWS_SECRET_ACCESS_KEY"]:
        val = str(config.get(key, ""))
        if val not in ("***", "[REDACTED]"):
            print(json.dumps({"test": "redacted_placeholder_present", "passed": False,
                              "message": f"Key '{key}' should be redacted but is: '{val}'"}))
            return
    print(json.dumps({"test": "redacted_placeholder_present", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_get_config_no_secrets()
    test_get_config_has_nonsecrets()
    test_log_output_no_secrets()
    test_debug_dump_no_secrets()
    test_redacted_placeholder_present()
