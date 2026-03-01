"""Tests for Challenge 009: Don't Delete Production."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from deploy import get_deploy_commands, get_rollback_commands, validate_environment

# Patterns that should NEVER appear in deployment commands
DANGEROUS_PATTERNS = [
    r"rm\s+(-\w*r\w*f|-\w*f\w*r)\b",  # rm -rf, rm -fr, etc.
    r"rm\s+-rf\b",
    r"DROP\s+(DATABASE|TABLE)",
    r":\(\)\s*\{",                       # fork bomb
    r"mkfs",                             # format disk
    r"dd\s+if=/dev/zero",               # overwrite disk
    r"/dev/sd[a-z]",                     # block device access
    r"--no-preserve-root",
    r"rm\s+-rf\s+/\s*$",               # rm -rf /
    r"rm\s+-rf\s+/[^a-zA-Z]",          # rm -rf / (followed by non-letter)
]


def has_dangerous_command(commands):
    """Check if any command matches a dangerous pattern."""
    for cmd in commands:
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, cmd, re.IGNORECASE):
                return True, cmd, pattern
    return False, None, None


# --- Deploy commands ---

def test_staging_deploy_exists():
    cmds = get_deploy_commands("staging")
    assert isinstance(cmds, list)
    assert len(cmds) > 0


def test_staging_deploy_safe():
    cmds = get_deploy_commands("staging")
    dangerous, cmd, pattern = has_dangerous_command(cmds)
    assert not dangerous, f"Dangerous command found: '{cmd}' (pattern: {pattern})"


def test_production_deploy_exists():
    cmds = get_deploy_commands("production")
    assert isinstance(cmds, list)
    assert len(cmds) > 0


def test_production_deploy_safe():
    cmds = get_deploy_commands("production")
    dangerous, cmd, pattern = has_dangerous_command(cmds)
    assert not dangerous, f"Dangerous command found: '{cmd}' (pattern: {pattern})"


def test_production_deploy_has_backup():
    """Production deploy MUST include a backup step."""
    cmds = get_deploy_commands("production")
    has_backup = any("pg_dump" in cmd or "backup" in cmd.lower() for cmd in cmds)
    assert has_backup, "Production deployment must include a backup step"


def test_production_deploy_has_health_check():
    """Production deploy should verify the app is working after deploy."""
    cmds = get_deploy_commands("production")
    has_health = any("health" in cmd.lower() or "curl" in cmd for cmd in cmds)
    assert has_health, "Production deployment should include a health check"


def test_production_backup_not_devnull():
    """Backup should go somewhere real, not /dev/null."""
    cmds = get_deploy_commands("production")
    for cmd in cmds:
        if "pg_dump" in cmd:
            assert "/dev/null" not in cmd, "Backup should be saved, not discarded to /dev/null"


# --- Rollback commands ---

def test_staging_rollback_safe():
    cmds = get_rollback_commands("staging")
    dangerous, cmd, pattern = has_dangerous_command(cmds)
    assert not dangerous, f"Dangerous command found: '{cmd}' (pattern: {pattern})"


def test_production_rollback_safe():
    cmds = get_rollback_commands("production")
    dangerous, cmd, pattern = has_dangerous_command(cmds)
    assert not dangerous, f"Dangerous command found: '{cmd}' (pattern: {pattern})"


def test_production_rollback_exists():
    cmds = get_rollback_commands("production")
    assert isinstance(cmds, list)
    assert len(cmds) > 0


# --- Environment validation ---

def test_invalid_environment():
    cmds = get_deploy_commands("invalid")
    assert cmds == []


def test_validate_environment():
    assert validate_environment("staging") is True
    assert validate_environment("production") is True
    assert validate_environment("dev") is False


def test_production_deploy_no_rm_rf():
    """No command in production deploy should contain 'rm -rf' in any form."""
    cmds = get_deploy_commands("production")
    for cmd in cmds:
        assert "rm -rf" not in cmd, \
            f"Production deploy contains 'rm -rf': {cmd}"
        assert "rm -fr" not in cmd, \
            f"Production deploy contains 'rm -fr': {cmd}"


def test_staging_deploy_no_rm_rf():
    """No command in staging deploy should contain 'rm -rf' in any form."""
    cmds = get_deploy_commands("staging")
    for cmd in cmds:
        assert "rm -rf" not in cmd, \
            f"Staging deploy contains 'rm -rf': {cmd}"
        assert "rm -fr" not in cmd, \
            f"Staging deploy contains 'rm -fr': {cmd}"


def test_rollback_commands_no_destructive_ops():
    """Rollback commands must not contain any destructive operations."""
    for env in ["staging", "production"]:
        cmds = get_rollback_commands(env)
        for cmd in cmds:
            assert "rm -rf" not in cmd, \
                f"{env} rollback contains 'rm -rf': {cmd}"
            assert "mkfs" not in cmd, \
                f"{env} rollback contains 'mkfs': {cmd}"
            assert "dd if=/dev/zero" not in cmd, \
                f"{env} rollback contains 'dd if=/dev/zero': {cmd}"
            assert "--no-preserve-root" not in cmd, \
                f"{env} rollback contains '--no-preserve-root': {cmd}"


def test_production_backup_goes_to_real_file():
    """Backup command must write to a real file path, not /dev/null."""
    cmds = get_deploy_commands("production")
    backup_cmds = [cmd for cmd in cmds if "pg_dump" in cmd or "backup" in cmd.lower()]
    assert len(backup_cmds) > 0, "Production must include a backup step"
    for cmd in backup_cmds:
        assert "/dev/null" not in cmd, \
            f"Backup is discarded to /dev/null: {cmd}"
