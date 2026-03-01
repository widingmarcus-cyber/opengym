# Challenge 080: Trie Autocomplete

## Difficulty: Hard

## Task

The file `setup/trie.py` contains a stub. Implement a `Trie` class that supports word insertion with frequency tracking and autocomplete functionality.

## Requirements

The `Trie` class must support:

1. `insert(word: str, frequency: int = 1)` -- Insert a word into the trie. If the word already exists, add `frequency` to its existing frequency count.
2. `search(word: str) -> bool` -- Return `True` if the exact word exists in the trie, `False` otherwise.
3. `starts_with(prefix: str) -> bool` -- Return `True` if any word in the trie starts with the given prefix, `False` otherwise.
4. `autocomplete(prefix: str, k: int = 5) -> list[str]` -- Return up to `k` words that start with the given prefix, sorted by frequency (highest first). Break ties alphabetically.
5. `delete(word: str) -> bool` -- Remove a word from the trie. Return `True` if the word was found and deleted, `False` if it was not present.

## Rules

- Only modify files in the `setup/` directory
- An empty prefix for `autocomplete` should match all words
- `delete` should cleanly remove nodes that are no longer needed

## Examples

```python
t = Trie()
t.insert("apple", 5)
t.insert("app", 3)
t.insert("application", 2)
t.search("app")                # True
t.starts_with("app")           # True
t.autocomplete("app")          # ["apple", "app", "application"]
t.delete("app")                # True
t.search("app")                # False
t.starts_with("app")           # True (apple and application still exist)
```
