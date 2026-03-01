# Challenge 096: Feature Flag Rollout

## Difficulty: Medium

## Task

Implement a feature flag system and wire it into a simple application. The agent must implement the `FeatureFlags` class in `setup/flags.py` and update `setup/app.py` to gate its features using the flag system.

## Setup

- `setup/flags.py` -- Stub for the `FeatureFlags` class.
- `setup/app.py` -- A simple app with 3 feature functions that must be gated by flags.
- `setup/config.json` -- Feature flag configuration.

## Requirements

### FeatureFlags class (`flags.py`)

1. `FeatureFlags(config_path=None)` -- Constructor. Optionally loads initial flag state from a JSON config file.
2. `is_enabled(flag_name, user_id=None) -> bool` -- Check if a flag is enabled. If a rollout percentage is set for the flag and `user_id` is provided, deterministically decide based on `hash(user_id) % 100 < percentage`. If no `user_id`, return `True` only if the flag is fully enabled (100% or explicitly enabled).
3. `enable(flag_name)` -- Enable a flag globally (100%).
4. `disable(flag_name)` -- Disable a flag globally (0%).
5. `set_rollout_percentage(flag_name, pct)` -- Set the rollout percentage (0-100) for a flag.
6. `get_all_flags() -> dict` -- Return a dict of all flags and their current state.

### App functions (`app.py`)

The app has three functions that should check flags before executing:

1. `new_dashboard(flags, user_id=None)` -- Returns `"new dashboard"` if the `new_dashboard` flag is enabled, else `"classic dashboard"`.
2. `dark_mode(flags, user_id=None)` -- Returns `"dark"` if the `dark_mode` flag is enabled, else `"light"`.
3. `export_csv(flags, data, user_id=None)` -- Returns `"exported: <data>"` if the `export_csv` flag is enabled, else `"export disabled"`.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.
