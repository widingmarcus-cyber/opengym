"""
Application configuration and diagnostics module.
"""

import os
import io
import logging

# Configure logging to a string buffer so tests can capture output
log_stream = io.StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger("app")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


SECRET_KEYS = {"DATABASE_PASSWORD", "API_SECRET_KEY", "AWS_SECRET_ACCESS_KEY"}


def get_config():
    """
    Return the full application configuration as a dict.
    """
    config = {
        "APP_NAME": os.environ.get("APP_NAME", "myapp"),
        "APP_ENV": os.environ.get("APP_ENV", "production"),
        "DEBUG": os.environ.get("DEBUG", "false"),
        "DATABASE_PASSWORD": os.environ.get("DATABASE_PASSWORD", "s3cret_db_pass"),
        "API_SECRET_KEY": os.environ.get("API_SECRET_KEY", "sk-abc123secret"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY", "AKIASECRETKEY999"),
    }
    return config


def log_startup_info():
    """
    Log application startup information.
    """
    config = get_config()
    for key, value in config.items():
        logger.info(f"Config: {key} = {value}")
    return log_stream.getvalue()


def get_debug_dump():
    """
    Return a debug dump string with all environment info.
    """
    config = get_config()
    lines = []
    for key, value in config.items():
        lines.append(f"{key}={value}")
    return "\n".join(lines)
