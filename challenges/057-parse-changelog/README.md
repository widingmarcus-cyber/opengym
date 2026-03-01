# Challenge 057: Parse Changelog

## Difficulty: Easy

## Task

Extract information from a realistic CHANGELOG.md file. Implement the functions in `setup/answers.py`.

## Setup

`setup/CHANGELOG.md` contains a changelog spanning 20 releases with version numbers, dates, breaking changes, new features, and bug fixes.

## Requirements

Implement all functions in `setup/answers.py`:

1. `latest_version()` — Return the latest version string (e.g., `"2.5.0"`)
2. `total_releases()` — Return the total number of releases (int)
3. `breaking_changes_count()` — Return the total number of individual breaking change items across all releases (int)
4. `first_release_date()` — Return the date of the earliest release as a string (e.g., `"2022-01-15"`)
5. `features_in_version(version)` — Return a list of feature descriptions for the given version (list of str)
6. `versions_with_breaking_changes()` — Return a sorted list of version strings that contain breaking changes (list of str, sorted ascending)

## Rules

- Only modify `setup/answers.py`
- Parse the CHANGELOG.md file to extract answers
- Version strings should not include the `v` prefix
