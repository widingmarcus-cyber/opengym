# Challenge 056: Search the Codebase

## Difficulty: Easy

## Task

Read and analyze the mini codebase in `setup/project/` and answer questions about it by implementing the functions in `setup/answers.py`.

## Setup

The `setup/project/` directory contains 6 Python files forming a small web application:
- `app.py` — Application entry point
- `routes.py` — Route handlers
- `models.py` — Data models
- `utils.py` — Utility functions
- `config.py` — Configuration
- `database.py` — Database connection layer

## Requirements

Implement all functions in `setup/answers.py`. Each function answers a specific question about the codebase:

1. `how_many_functions()` — Return the total number of `def` function/method definitions across all 6 files (int)
2. `what_is_the_entry_point()` — Return the filename that serves as the application entry point (str)
3. `list_all_imports()` — Return a sorted list of all unique module names imported across the project (list of str)
4. `which_file_has_most_lines()` — Return the filename with the most lines of code (str)
5. `list_all_classes()` — Return a sorted list of all class names defined in the project (list of str)
6. `what_database_engine()` — Return the database engine string used in the configuration (str)
7. `how_many_routes()` — Return the number of route handler functions defined (int)
8. `find_todo_comments()` — Return a sorted list of all TODO comment texts (list of str)

## Rules

- Only modify `setup/answers.py`
- Return exact values that match the codebase contents
- Filenames should be just the basename (e.g., `"app.py"`, not the full path)
