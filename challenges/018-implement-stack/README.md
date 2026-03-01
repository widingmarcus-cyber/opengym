# Challenge 018: Implement Stack

## Difficulty: Easy

## Task

The file `setup/stack.py` is empty. Implement a `Stack` class that provides a standard LIFO (last-in, first-out) data structure.

## Requirements

The `Stack` class must support:

1. `push(item)` — Push an item onto the top of the stack
2. `pop()` — Remove and return the top item. Raise `IndexError` if the stack is empty
3. `peek()` — Return the top item without removing it. Raise `IndexError` if the stack is empty
4. `is_empty()` — Return `True` if the stack has no items, `False` otherwise
5. `size()` — Return the number of items in the stack
6. `__iter__` — Iterate over items from top to bottom

## Rules

- Only modify files in the `setup/` directory
- All methods must behave exactly as specified above
- The stack should work with any type of item

## Examples

```python
s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.peek()        # 3
s.pop()         # 3
s.size()        # 2
s.is_empty()    # False
list(s)         # [2, 1]
```
