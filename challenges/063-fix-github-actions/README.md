# Challenge 063: Fix GitHub Actions Workflow

## Difficulty: Easy

## Task

The file `setup/ci.yml` is a broken GitHub Actions workflow configuration. Fix all the issues so that it defines a valid CI pipeline.

## Setup

- `setup/ci.yml` — A broken GitHub Actions workflow file that needs to be fixed

## Requirements

Fix the workflow file so that:

1. The YAML is valid and properly indented
2. The workflow triggers on push to the `main` branch (at minimum)
3. The runner uses a current Ubuntu version (e.g., `ubuntu-latest` or `ubuntu-22.04`)
4. The job includes a checkout step using `actions/checkout`
5. The job includes a step to set up Python using `actions/setup-python`
6. The job includes a step to install dependencies (pip install)
7. The job includes a step to run tests (pytest)
8. All steps have proper `uses:` or `run:` fields

## Rules

- Only modify `setup/ci.yml`
- The resulting file must be valid YAML
- Follow GitHub Actions workflow syntax
