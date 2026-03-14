"""Predefined challenge profiles for infra-focused benchmark runs."""

from __future__ import annotations

from pathlib import Path

import yaml

PROFILE_NAMES = (
    "infra-smoke",
    "infra-weekly",
    "infra-nightly",
    "infra-hard",
    "safety-gate",
)

_DIFFICULTY_RANK = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
}


def _load_challenges(challenges_dir: Path) -> list[dict]:
    """Load all challenge metadata with resolved folder IDs."""
    loaded: list[dict] = []
    for challenge_dir in sorted(challenges_dir.iterdir()):
        meta_file = challenge_dir / "metadata.yaml"
        if not challenge_dir.is_dir() or not meta_file.exists():
            continue
        with open(meta_file, encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}
        loaded.append({"id": challenge_dir.name, "meta": meta})
    return loaded


def _hardness_sorted(challenges: list[dict]) -> list[dict]:
    """Sort by inferred hardness (difficulty, then cost, then challenge id)."""
    return sorted(
        challenges,
        key=lambda item: (
            -_DIFFICULTY_RANK.get(
                str(item["meta"].get("difficulty", "easy")).lower(), 0
            ),
            -float(item["meta"].get("estimated_cost_usd", 0.0) or 0.0),
            item["id"],
        ),
    )


def _infra_only(challenges: list[dict]) -> list[dict]:
    """Filter for infra-conformance challenges."""
    return [
        item
        for item in challenges
        if item["meta"].get("challenge_type") == "INFRA_CONFORMANCE"
    ]


def resolve_profile_ids(profile: str, challenges_dir: Path) -> list[str]:
    """Resolve a profile name to concrete challenge IDs."""
    profile_key = profile.lower()
    if profile_key not in PROFILE_NAMES:
        return []

    all_challenges = _load_challenges(challenges_dir)
    infra = _infra_only(all_challenges)

    if profile_key == "infra-nightly":
        return sorted(item["id"] for item in infra)

    if profile_key == "infra-hard":
        hard = [
            item
            for item in infra
            if str(item["meta"].get("difficulty", "")).lower() == "hard"
        ]
        return sorted(item["id"] for item in hard)

    if profile_key == "infra-weekly":
        hardest = _hardness_sorted(infra)[:60]
        return sorted(item["id"] for item in hardest)

    if profile_key == "safety-gate":
        target_categories = {
            "security-boundary",
            "prompt-injection",
            "destructive-command",
            "data-exfiltration",
            "scope-boundaries",
            "failure-recovery",
            "fault-tolerance",
            "adaptive-recovery",
        }
        scoped = [
            item
            for item in infra
            if item["meta"].get("dimension") in {"safety", "resilience"}
            or item["meta"].get("category") in target_categories
        ]
        return sorted(item["id"] for item in scoped)

    # infra-smoke:
    # one representative per infra dimension (hardest-first), then fill to 12.
    target_dims = [
        "memory",
        "tool-use",
        "resilience",
        "safety",
        "multi-agent",
        "planning",
    ]
    sorted_infra = _hardness_sorted(infra)
    picked: dict[str, dict] = {}
    for dim in target_dims:
        for item in sorted_infra:
            if item["meta"].get("dimension") == dim:
                picked[item["id"]] = item
                break

    for item in sorted_infra:
        if len(picked) >= 12:
            break
        picked.setdefault(item["id"], item)

    return sorted(picked)
