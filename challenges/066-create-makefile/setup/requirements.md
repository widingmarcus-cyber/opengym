# Makefile Requirements

## Targets

### `install`
- Command: `pip install -r requirements.txt`
- No dependencies

### `test`
- Command: `pytest tests/ -v`
- Depends on: `install`

### `lint`
- Command: `flake8 src/`
- Depends on: `install`

### `format`
- Command: `black src/ tests/`
- Depends on: `install`

### `clean`
- Command: `rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache`
- No dependencies

### `build`
- Command: `python -m build`
- Depends on: `test` and `lint`

### `deploy`
- Command: `twine upload dist/*`
- Depends on: `test` and `build`

## Notes

- All targets should be declared as `.PHONY` since none of them produce files
- The default target (first target or `all`) is not required
