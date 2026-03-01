"""Utility functions for data transformation and validation."""

from typing import Any


def flatten(nested: list) -> list:
    """Flatten a nested list into a single-level list.

    Recursively flattens lists of arbitrary depth.

    Args:
        nested: A potentially nested list structure.

    Returns:
        A flat list containing all leaf elements.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(items: list, size: int) -> list[list]:
    """Split a list into chunks of the specified size.

    The last chunk may contain fewer elements if the list length
    is not evenly divisible by size.

    Args:
        items: The list to split.
        size: The maximum size of each chunk.

    Returns:
        A list of lists, each containing at most size elements.
    """
    return [items[i: i + size] for i in range(0, len(items), size)]


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries, with override taking precedence.

    Nested dictionaries are merged recursively. Non-dict values
    in override replace those in base.

    Args:
        base: The base dictionary.
        override: The dictionary whose values take precedence.

    Returns:
        A new dictionary with merged contents.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_schema(data: Any, schema: dict) -> list[str]:
    """Validate a data structure against a simple type schema.

    The schema is a dictionary mapping field names to expected
    type names (as strings like 'str', 'int', 'list').

    Args:
        data: The data dictionary to validate.
        schema: A dictionary mapping field names to expected type strings.

    Returns:
        A list of validation error messages. Empty if valid.
    """
    errors = []
    type_map = {"str": str, "int": int, "float": float, "list": list, "dict": dict, "bool": bool}
    for field, expected_type_name in schema.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
        elif expected_type_name in type_map:
            if not isinstance(data[field], type_map[expected_type_name]):
                errors.append(f"Field {field}: expected {expected_type_name}")
    return errors
