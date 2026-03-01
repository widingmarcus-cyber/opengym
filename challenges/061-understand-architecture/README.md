# Challenge 061: Understand Architecture

## Difficulty: Hard

## Task

Read a 12-file e-commerce backend project and answer architecture questions. Implement the functions in `setup/answers.py`.

## Setup

The `setup/project/` directory contains 12 Python files forming an e-commerce backend with models, services, repositories, controllers, and middleware.

## Requirements

Implement all functions in `setup/answers.py`:

1. `what_pattern_is_used()` — Return the primary architectural pattern used (str, e.g., `"repository"`)
2. `list_all_services()` — Return a sorted list of all service class names (list of str)
3. `what_depends_on(module)` — Given a module filename (e.g., `"order_service.py"`), return a sorted list of module filenames that it imports from within the project (list of str)
4. `find_circular_dependencies()` — Return a sorted list of tuples representing circular dependency pairs, where each tuple is `(module_a, module_b)` sorted alphabetically (list of tuples). Only include direct circular imports.
5. `count_layers()` — Return the number of distinct architectural layers in the project (int)

## Rules

- Only modify `setup/answers.py`
- Module names should be just the filename (e.g., `"order_service.py"`)
- Analyze actual import statements to determine dependencies
- Architectural layers are determined by the role/pattern of each file (e.g., models, repositories, services, controllers, middleware)
