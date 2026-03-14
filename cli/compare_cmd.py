"""Compare two OpenGym JSON reports and highlight regressions/improvements."""

from __future__ import annotations

import json
from pathlib import Path

import click


def _load_payload(path: Path) -> tuple[dict, dict]:
    """Load either a raw report or wrapped save-report payload."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and isinstance(data.get("report"), dict):
        return data["report"], data.get("metadata", {})
    if isinstance(data, dict):
        return data, {}
    raise ValueError(f"Invalid report JSON format: {path}")


def _extract_total_score(report: dict) -> int:
    if isinstance(report.get("total_score"), int):
        return int(report["total_score"])
    if isinstance(report.get("overall_score"), int):
        return int(report["overall_score"])
    return 0


def _extract_pass_counts(report: dict) -> tuple[int, int]:
    passed = report.get("passed")
    total = report.get("challenges_attempted")
    if isinstance(passed, int) and isinstance(total, int):
        return passed, total

    infra_passed = report.get("infra_passed")
    infra_total = report.get("infra_total")
    model_passed = report.get("model_passed")
    model_total = report.get("model_total")
    if all(
        isinstance(v, int)
        for v in [infra_passed, infra_total, model_passed, model_total]
    ):
        return infra_passed + model_passed, infra_total + model_total

    return 0, 0


def _extract_dimension_scores(report: dict) -> dict[str, int]:
    raw = report.get("by_dimension", {})
    if not isinstance(raw, dict):
        return {}

    parsed: dict[str, int] = {}
    for dim, value in raw.items():
        if isinstance(value, dict):
            score = value.get("score")
        else:
            score = value
        if isinstance(score, (int, float)):
            parsed[dim] = int(round(score))
    return parsed


def _extract_reliability(report: dict) -> dict:
    rel = report.get("reliability")
    return rel if isinstance(rel, dict) else {}


def _reliability_status_index(rel: dict) -> dict[str, dict]:
    rows = rel.get("by_challenge", [])
    if not isinstance(rows, list):
        return {}

    idx: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        cid = row.get("challenge")
        if isinstance(cid, str):
            idx[cid] = row
    return idx


def _safe_pct(value: object) -> float:
    return float(value) if isinstance(value, (int, float)) else 0.0


@click.command(name="compare")
@click.argument("baseline_json")
@click.argument("current_json")
@click.option("--json-output", is_flag=True, help="Output comparison as JSON")
@click.option(
    "--top",
    type=click.IntRange(1),
    default=12,
    show_default=True,
    help="Maximum number of status changes to print in text mode.",
)
def compare_reports(baseline_json: str, current_json: str, json_output: bool, top: int):
    """Compare two report JSON files (baseline first, current second)."""
    baseline_path = Path(baseline_json).expanduser().resolve()
    current_path = Path(current_json).expanduser().resolve()

    try:
        baseline_report, baseline_meta = _load_payload(baseline_path)
        current_report, current_meta = _load_payload(current_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise click.ClickException(str(exc)) from exc

    baseline_score = _extract_total_score(baseline_report)
    current_score = _extract_total_score(current_report)

    baseline_passed, baseline_total = _extract_pass_counts(baseline_report)
    current_passed, current_total = _extract_pass_counts(current_report)

    base_dims = _extract_dimension_scores(baseline_report)
    curr_dims = _extract_dimension_scores(current_report)
    all_dims = sorted(set(base_dims) | set(curr_dims))
    dimension_deltas = {
        dim: curr_dims.get(dim, 0) - base_dims.get(dim, 0) for dim in all_dims
    }

    base_rel = _extract_reliability(baseline_report)
    curr_rel = _extract_reliability(current_report)
    base_trial_pass = _safe_pct(base_rel.get("overall_trial_pass_rate_pct"))
    curr_trial_pass = _safe_pct(curr_rel.get("overall_trial_pass_rate_pct"))

    base_status = _reliability_status_index(base_rel)
    curr_status = _reliability_status_index(curr_rel)

    regressions: list[dict] = []
    improvements: list[dict] = []
    for cid in sorted(set(base_status) & set(curr_status)):
        before = str(base_status[cid].get("status", "unknown"))
        after = str(curr_status[cid].get("status", "unknown"))
        if before == after:
            continue
        event = {
            "challenge": cid,
            "name": curr_status[cid].get("name") or base_status[cid].get("name") or cid,
            "from": before,
            "to": after,
            "before_pass_rate_pct": _safe_pct(base_status[cid].get("pass_rate_pct")),
            "after_pass_rate_pct": _safe_pct(curr_status[cid].get("pass_rate_pct")),
        }
        if (before, after) in {
            ("stable", "flaky"),
            ("stable", "broken"),
            ("flaky", "broken"),
        }:
            regressions.append(event)
        elif (before, after) in {
            ("broken", "flaky"),
            ("broken", "stable"),
            ("flaky", "stable"),
        }:
            improvements.append(event)

    result = {
        "baseline_file": str(baseline_path),
        "current_file": str(current_path),
        "baseline_generated_at_utc": baseline_meta.get("generated_at_utc"),
        "current_generated_at_utc": current_meta.get("generated_at_utc"),
        "delta": {
            "total_score": current_score - baseline_score,
            "passed": current_passed - baseline_passed,
            "challenge_count": current_total - baseline_total,
            "trial_pass_rate_pct": round(curr_trial_pass - base_trial_pass, 1),
            "stable_challenges": int(curr_rel.get("stable_challenges", 0))
            - int(base_rel.get("stable_challenges", 0)),
            "flaky_challenges": int(curr_rel.get("flaky_challenges", 0))
            - int(base_rel.get("flaky_challenges", 0)),
            "broken_challenges": int(curr_rel.get("broken_challenges", 0))
            - int(base_rel.get("broken_challenges", 0)),
            "by_dimension": dimension_deltas,
        },
        "regressions": regressions,
        "improvements": improvements,
    }

    if json_output:
        click.echo(json.dumps(result, indent=2))
        return

    click.echo("\n==================================================")
    click.echo("OpenGym Report Comparison")
    click.echo("==================================================")
    click.echo(f"Baseline: {baseline_path}")
    click.echo(f"Current:  {current_path}")
    click.echo("")
    click.echo(
        f"Total Score: {baseline_score} -> {current_score} ({current_score - baseline_score:+d})"
    )
    if baseline_total or current_total:
        click.echo(
            f"Passes:      {baseline_passed}/{baseline_total} -> {current_passed}/{current_total} ({current_passed - baseline_passed:+d})"
        )
    if base_rel or curr_rel:
        click.echo(
            f"Trial Pass%: {base_trial_pass:.1f}% -> {curr_trial_pass:.1f}% ({curr_trial_pass - base_trial_pass:+.1f})"
        )
        click.echo(
            "Stability:   "
            f"stable {result['delta']['stable_challenges']:+d}, "
            f"flaky {result['delta']['flaky_challenges']:+d}, "
            f"broken {result['delta']['broken_challenges']:+d}"
        )

    if dimension_deltas:
        click.echo("\nDimension Deltas:")
        for dim, delta in sorted(
            dimension_deltas.items(), key=lambda item: (item[1], item[0])
        ):
            click.echo(f"  {dim:<14} {delta:+d}")

    if regressions:
        click.echo("\nRegressions:")
        for row in regressions[:top]:
            click.echo(
                "  "
                f"{row['challenge']} {row['name']}: "
                f"{row['from']} -> {row['to']} "
                f"({row['before_pass_rate_pct']:.1f}% -> {row['after_pass_rate_pct']:.1f}%)"
            )
        if len(regressions) > top:
            click.echo(f"  ... and {len(regressions) - top} more")

    if improvements:
        click.echo("\nImprovements:")
        for row in improvements[:top]:
            click.echo(
                "  "
                f"{row['challenge']} {row['name']}: "
                f"{row['from']} -> {row['to']} "
                f"({row['before_pass_rate_pct']:.1f}% -> {row['after_pass_rate_pct']:.1f}%)"
            )
        if len(improvements) > top:
            click.echo(f"  ... and {len(improvements) - top} more")

    if not regressions and not improvements:
        click.echo("\nNo reliability status transitions detected.")
