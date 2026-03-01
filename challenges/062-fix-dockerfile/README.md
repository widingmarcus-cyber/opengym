# Challenge 062: Fix Dockerfile

## Difficulty: Easy

## Task

The file `setup/Dockerfile` is broken and will not build correctly. Fix all the issues so the Dockerfile correctly containerizes the Flask application in `setup/app.py`.

## Setup

- `setup/Dockerfile` — A broken Dockerfile that needs to be fixed
- `setup/app.py` — A simple Flask application (do not modify)

## Requirements

Fix the Dockerfile so that:

1. It uses an appropriate Python 3.x base image (slim variant preferred)
2. The working directory is set before any COPY instructions
3. Dependencies are properly installed via pip (flask must be installed)
4. A `requirements.txt` is created or the install command installs flask directly
5. The CMD instruction uses valid exec-form syntax to run the app
6. The overall instruction ordering follows Dockerfile best practices

## Rules

- Only modify `setup/Dockerfile`
- Do not modify `setup/app.py`
- The resulting Dockerfile must follow standard best practices
