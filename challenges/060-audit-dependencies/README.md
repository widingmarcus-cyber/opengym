# Challenge 060: Audit Dependencies

## Difficulty: Hard

## Task

Analyze Python dependency files for conflicts, vulnerabilities, and issues. Implement the functions in `setup/audit.py`.

## Setup

Three files are provided:
- `setup/requirements.txt` — pip requirements with version pins
- `setup/setup.cfg` — setuptools configuration with `install_requires`
- `setup/known_vulnerabilities.json` — list of known vulnerabilities with package, version, and CVE info

## Requirements

Implement all functions in `setup/audit.py`:

1. `find_conflicts(req_path, setup_path)` — Find packages that appear in both files with different version specifications. Return a sorted list of dicts: `[{"package": str, "requirements_spec": str, "setup_spec": str}, ...]`
2. `find_vulnerable(req_path, vuln_path)` — Find packages in requirements.txt that match known vulnerabilities. Return a sorted list of dicts: `[{"package": str, "version": str, "cve": str}, ...]`
3. `find_unpinned(req_path)` — Find packages in requirements.txt that do not have a version pin (no `==`, `>=`, `<=`, `!=`, `~=`, `>`, `<`). Return a sorted list of package names (list of str).

## Rules

- Only modify `setup/audit.py`
- Parse the files to extract dependency information
- Version matching for vulnerabilities should compare the exact pinned version (`==`) against the vulnerability database
- Sort results by package name
