"""List available challenges."""

import json

import click
import yaml

from cli.utils import get_challenges_dir


@click.command()
@click.option("--category", "-c", default=None, help="Filter by category")
@click.option("--dimension", "-D", default=None, help="Filter by dimension (coding/memory/tool-use/resilience/safety/multi-agent/planning)")
@click.option("--difficulty", "-d", default=None, help="Filter by difficulty (easy/medium/hard)")
@click.option("--json-output", is_flag=True, help="Output as JSON")
def list_challenges(category: str | None, dimension: str | None, difficulty: str | None, json_output: bool):
    """List all available challenges."""
    challenges_dir = get_challenges_dir()

    challenges = []
    for challenge_path in sorted(challenges_dir.iterdir()):
        meta_file = challenge_path / "metadata.yaml"
        if not meta_file.exists():
            continue

        with open(meta_file) as f:
            meta = yaml.safe_load(f)

        if category and meta.get("category") != category:
            continue
        if dimension and meta.get("dimension") != dimension:
            continue
        if difficulty and meta.get("difficulty") != difficulty:
            continue

        challenges.append({
            "id": meta["id"],
            "name": meta["name"],
            "difficulty": meta["difficulty"],
            "category": meta["category"],
            "dimension": meta.get("dimension", "coding"),
            "language": meta.get("language", "python"),
        })

    if json_output:
        click.echo(json.dumps(challenges, indent=2))
        return

    if not challenges:
        click.echo("No challenges found matching your filters.")
        return

    # Table output
    click.echo(f"{'ID':<6} {'Name':<30} {'Difficulty':<10} {'Dimension':<12} {'Category':<15}")
    click.echo("-" * 76)
    for c in challenges:
        click.echo(f"{c['id']:<6} {c['name']:<30} {c['difficulty']:<10} {c['dimension']:<12} {c['category']:<15}")

    click.echo(f"\n{len(challenges)} challenge(s) available.")
