def validate_input(value):
    if not isinstance(value, str):
        raise TypeError("Expected string")
    return True