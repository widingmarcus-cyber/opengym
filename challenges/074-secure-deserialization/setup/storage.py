"""Data storage using pickle serialization."""

import pickle


def save(data, filepath):
    """Save data to a file.

    Args:
        data: The data to serialize and save.
        filepath: Path to the output file.
    """
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


def load(filepath):
    """Load data from a file.

    Args:
        filepath: Path to the file to load.

    Returns:
        The deserialized data.
    """
    with open(filepath, "rb") as f:
        return pickle.load(f)
