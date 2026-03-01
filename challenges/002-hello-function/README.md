# Challenge 002: Hello Function

## Difficulty: Easy

## Task

The file `setup/greeter.py` is empty. Write a module with the following functions:

1. `greet(name)` — Returns `"Hello, {name}!"`
2. `greet_many(names)` — Takes a list of names, returns a list of greetings
3. `formal_greet(name, title="Mr.")` — Returns `"Good day, {title} {name}."`

## Rules

- Only modify files in the `setup/` directory
- Follow the exact output format shown above
- Handle edge cases: empty string name should return `"Hello, !"`

## Examples

```python
greet("Alice")                    # "Hello, Alice!"
greet_many(["Alice", "Bob"])      # ["Hello, Alice!", "Hello, Bob!"]
formal_greet("Smith")             # "Good day, Mr. Smith."
formal_greet("Smith", title="Dr.")  # "Good day, Dr. Smith."
```
