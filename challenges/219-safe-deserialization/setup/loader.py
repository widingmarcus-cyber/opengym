"""
Data loading/deserialization module.
"""

import json
import pickle


def load_config(data_bytes):
    """
    Load configuration from bytes.

    Args:
        data_bytes: Bytes containing serialized configuration data.

    Returns:
        dict with "status" and either "data" or "message"
    """
    try:
        config = pickle.loads(data_bytes)
        return {"status": "ok", "data": config}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def parse_user_input(input_string):
    """
    Parse user-provided data string into a Python object.

    Args:
        input_string: A string representation of a Python literal.

    Returns:
        dict with "status" and either "data" or "message"
    """
    try:
        data = eval(input_string)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def load_message(json_string):
    """
    Load a message from a JSON string. (Already safe — do NOT modify.)

    Args:
        json_string: A JSON-encoded string.

    Returns:
        dict with "status" and either "data" or "message"
    """
    try:
        data = json.loads(json_string)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
