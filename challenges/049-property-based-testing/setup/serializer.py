"""A custom serialization library supporting basic Python types."""


def encode(data):
    """Encode a Python value into a string representation.

    Supports: str, int, float, bool, list, dict, None.
    """
    if data is None:
        return "N:"
    if isinstance(data, bool):
        return f"B:{'1' if data else '0'}"
    if isinstance(data, int):
        return f"I:{data}"
    if isinstance(data, float):
        return f"F:{data!r}"
    if isinstance(data, str):
        escaped = data.replace("\\", "\\\\").replace("|", "\\|")
        return f"S:{escaped}"
    if isinstance(data, list):
        parts = [encode(item) for item in data]
        return "L:" + "|".join(parts)
    if isinstance(data, dict):
        parts = []
        for key, value in data.items():
            parts.append(f"{encode(key)}={encode(value)}")
        return "D:" + "|".join(parts)
    raise TypeError(f"Unsupported type: {type(data)}")


def decode(encoded):
    """Decode a string representation back into a Python value.

    Supports: str, int, float, bool, list, dict, None.
    """
    if not isinstance(encoded, str):
        raise TypeError("Input must be a string")

    type_tag = encoded[:2]
    payload = encoded[2:]

    if type_tag == "N:":
        return None
    if type_tag == "B:":
        return payload == "1"
    if type_tag == "I:":
        return int(payload)
    if type_tag == "F:":
        return float(payload)
    if type_tag == "S:":
        return payload.replace("\\|", "|").replace("\\\\", "\\")
    if type_tag == "L:":
        if not payload:
            return []
        parts = _split_parts(payload)
        return [decode(part) for part in parts]
    if type_tag == "D:":
        if not payload:
            return {}
        result = {}
        entries = _split_parts(payload)
        for entry in entries:
            eq_pos = _find_separator(entry, "=")
            key_str = entry[:eq_pos]
            val_str = entry[eq_pos + 1:]
            result[decode(key_str)] = decode(val_str)
        return result
    raise ValueError(f"Unknown type tag: {type_tag}")


def _split_parts(text):
    """Split on unescaped pipe characters, respecting nesting."""
    parts = []
    current = []
    depth = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text):
            current.append(ch)
            current.append(text[i + 1])
            i += 2
            continue
        if ch in ("L", "D") and i + 1 < len(text) and text[i + 1] == ":":
            depth += 1
            current.append(ch)
        elif ch == "|" and depth == 0:
            parts.append("".join(current))
            current = []
            i += 1
            continue
        elif ch == "|" and depth > 0:
            depth -= 1
            current.append(ch)
        else:
            current.append(ch)
        i += 1
    if current:
        parts.append("".join(current))
    return parts


def _find_separator(text, sep):
    """Find the first unescaped occurrence of sep at depth 0."""
    depth = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text):
            i += 2
            continue
        if ch in ("L", "D") and i + 1 < len(text) and text[i + 1] == ":":
            depth += 1
        elif ch == "|" and depth > 0:
            depth -= 1
        elif ch == sep and depth == 0:
            return i
        i += 1
    raise ValueError(f"Separator '{sep}' not found in '{text}'")
