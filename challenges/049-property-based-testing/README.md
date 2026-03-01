# Challenge 049: Property-Based Testing

## Difficulty: Medium

## Task

The file `setup/serializer.py` contains a serialization library with `encode(data)` and `decode(encoded)` functions. These functions support serializing and deserializing: `str`, `int`, `float`, `bool`, `list`, `dict`, and `None`.

**Your job:** Write property-based tests in `setup/test_properties.py` that verify invariants of the serializer rather than just checking specific inputs/outputs.

## Key Properties to Test

1. **Round-trip**: `decode(encode(x)) == x` for all supported types
2. **Encode type**: `encode(x)` always returns a string
3. **Decode inverts encode**: For various generated inputs, encoding then decoding recovers the original
4. **Nested structures**: Round-trip works for nested lists and dicts
5. **Type preservation**: Decoded values have the same type as the original

## Rules

- Only modify files in the `setup/` directory
- Write your tests in `setup/test_properties.py`
- Use loops with generated test data to test many inputs (do not use the `hypothesis` library)
- You must write at least 6 test functions
- Each test should verify a property across multiple inputs, not just one example

## Examples

```python
# Round-trip property
for value in [42, "hello", 3.14, True, None, [1, 2], {"a": 1}]:
    assert decode(encode(value)) == value

# Encode always returns str
for value in [1, "test", [1, 2, 3]]:
    assert isinstance(encode(value), str)
```
