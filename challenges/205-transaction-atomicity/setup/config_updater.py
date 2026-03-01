"""Config updater — writes directly to config files with no atomicity.
If a write fails mid-way, configs are left in an inconsistent state.
Rewrite this script to make updates all-or-nothing."""

import json
import os

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SETUP_DIR, "config")

def update_configs(updates):
    """BAD: writes directly — no atomicity, no rollback."""
    for filename, new_data in updates.items():
        filepath = os.path.join(CONFIG_DIR, filename)
        # Direct write — if this crashes, file is corrupted
        with open(filepath, 'w') as f:
            json.dump(new_data, f, indent=2)

if __name__ == "__main__":
    with open(os.path.join(SETUP_DIR, "intended_update.json")) as f:
        updates = json.load(f)
    update_configs(updates)
