# Build and Wire the Plugin

**Difficulty:** Hard
**Category:** Multi-step
**Language:** Python

## Overview

The system has a plugin architecture with a base class, a registry, concrete plugins, and configuration. Your job is to complete the missing implementations so that everything works together end-to-end.

## What You Need To Do

1. **Complete the Plugin Registry** (`setup/registry.py`)
   - `register(plugin_class)` — register a plugin class by instantiating it and storing it by name
   - `get(name)` — return an instantiated plugin by name; raise `KeyError` if not found
   - `list_plugins()` — return a sorted list of registered plugin names
   - `create_pipeline(names)` — return a function that applies the named plugins in sequence to a text input

2. **Implement UppercasePlugin** (`setup/plugins/uppercase.py`)
   - Extend the `Plugin` base class
   - `name()` returns `"uppercase"`
   - `transform(text)` returns the text converted to uppercase

3. **Implement Configuration** (`setup/config.py`)
   - `load_config(config_dict)` — takes a dict with a `"plugins"` key listing plugin configurations; returns the parsed config
   - `setup_registry(config)` — creates a `PluginRegistry`, registers plugins from config, configures them with any provided settings, and returns the registry

## Files Provided

- `setup/plugin_base.py` — The `Plugin` abstract base class (already complete)
- `setup/registry.py` — Stub for `PluginRegistry` (you implement this)
- `setup/plugins/uppercase.py` — Stub for `UppercasePlugin` (you implement this)
- `setup/config.py` — Stub for config loading/setup (you implement this)

## Verification

```bash
pytest tests/ -v
```

All 10 tests must pass.
