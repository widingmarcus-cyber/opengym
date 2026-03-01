# Challenge 081: Expression Parser

## Difficulty: Hard

## Task

The file `setup/expression.py` contains a stub. Implement a mathematical expression evaluator that supports variables, operator precedence, and parentheses.

## Requirements

`evaluate(expr: str, variables: dict = None) -> float` -- Parse and evaluate a mathematical expression string. Return the result as a float.

Supported operations (in order of precedence, highest first):
1. `**` -- Exponentiation (right-associative)
2. Unary `-` -- Negation
3. `*`, `/` -- Multiplication and division (left-associative)
4. `+`, `-` -- Addition and subtraction (left-associative)

Additional features:
- Parentheses `()` for grouping
- Variable substitution from the `variables` dictionary
- Raise `ValueError` on invalid expressions (unbalanced parentheses, unknown variables, invalid syntax)

## Rules

- Only modify files in the `setup/` directory
- Do not use `eval()` or `exec()`
- Floating point results should be accurate to standard float precision

## Examples

```python
evaluate("2 + 3 * 4")           # 14.0
evaluate("(2 + 3) * 4")         # 20.0
evaluate("2 ** 3 ** 2")         # 512.0 (right-associative: 2 ** (3 ** 2))
evaluate("-3 + 4")              # 1.0
evaluate("x + y * 2", {"x": 3, "y": 5})  # 13.0
```
