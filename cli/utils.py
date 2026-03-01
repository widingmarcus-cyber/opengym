"""Shared utilities for the OpenGym CLI."""

from pathlib import Path


def get_project_root() -> Path:
    """Get the root of the opengym project (where pyproject.toml lives)."""
    # Walk up from this file to find pyproject.toml
    current = Path(__file__).resolve().parent.parent
    if (current / "pyproject.toml").exists():
        return current
    # Fallback: current working directory
    return Path.cwd()


def get_challenges_dir() -> Path:
    """Get the path to the challenges directory in the repo."""
    return get_project_root() / "challenges"


def get_workspace_dir() -> Path:
    """Get the default workspace directory where fetched challenges go."""
    workspace = Path.cwd() / "opengym-workspace"
    workspace.mkdir(exist_ok=True)
    return workspace


def resolve_challenge_ids(challenge_id: str, challenges_dir: Path) -> list[str]:
    """Resolve a challenge ID (number, name, or 'all') to a list of folder names."""
    if challenge_id == "all":
        return sorted([
            d.name for d in challenges_dir.iterdir()
            if d.is_dir() and (d / "metadata.yaml").exists()
        ])

    # Try exact folder name match
    if (challenges_dir / challenge_id).is_dir():
        return [challenge_id]

    # Try matching by number prefix (e.g., "001" matches "001-fix-syntax-error")
    padded = challenge_id.zfill(3)
    for d in challenges_dir.iterdir():
        if d.is_dir() and d.name.startswith(padded + "-"):
            return [d.name]

    # Try matching by partial name
    for d in challenges_dir.iterdir():
        if d.is_dir() and challenge_id in d.name:
            return [d.name]

    return []
