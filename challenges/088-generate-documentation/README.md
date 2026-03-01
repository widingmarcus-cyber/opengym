# Challenge 088: Generate Documentation

## Difficulty: Hard

## Task

Build a documentation generator that reads Python source files from a directory and produces clean Markdown documentation. Implement the generator in `setup/doc_generator.py`.

## Requirements

Implement this function in `setup/doc_generator.py`:

1. `generate_docs(source_dir)` -- Scan all `.py` files in the given directory, extract documentation information, and return a Markdown-formatted string.

### Extraction Rules

For each Python source file, extract:

- **Module name**: Derived from the filename (without `.py` extension).
- **Functions**: All top-level function definitions (`def` statements at module level).
- For each function, extract:
  - **Function signature**: The full `def` line including parameters and type annotations.
  - **Docstring**: The function's docstring (if present).
  - **Parameter types**: From type annotations in the signature.
  - **Return type**: From the return annotation (if present).

### Output Format

The generated Markdown should follow this structure:

```
# Module: <module_name>

## `function_name(param1: type1, param2: type2) -> return_type`

<docstring text>

## `another_function(param) -> type`

<docstring text>

# Module: <next_module_name>

...
```

- Each module gets a level-1 heading: `# Module: <name>`
- Each function gets a level-2 heading with its signature in backticks
- The docstring follows as plain text below the function heading
- Modules should be sorted alphabetically by name
- Functions within a module should appear in the order they are defined in the source

## Rules

- Only modify files in the `setup/` directory (do not modify files in `setup/source/`)
- Use only Python standard library modules (ast, inspect, etc.)
- Do not use Sphinx, pdoc, or any external documentation tools
