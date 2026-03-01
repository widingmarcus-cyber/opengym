"""Configuration loader."""


def load_config(data):
    """Load and return a configuration from a dictionary.

    Args:
        data: A dictionary with configuration keys:
              - host: Database host
              - port: Database port
              - database: Database name
              - data_dir: Path to data directory

    Returns:
        The validated configuration dictionary.
    """
    config = {
        "host": data.get("host", "localhost"),
        "port": data.get("port", 5432),
        "database": data.get("database", "mydb"),
        "data_dir": data.get("data_dir", "/var/data"),
    }
    return config
