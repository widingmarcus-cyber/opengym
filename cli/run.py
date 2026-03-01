"""Run an agent against challenges with multi-session orchestration."""

import json
import os
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from fnmatch import fnmatch
from pathlib import Path

import click
import yaml

from cli.utils import get_workspace_dir, resolve_challenge_ids, get_challenges_dir
from cli.score import score_challenge, build_summary, print_summary, build_scorecard, print_scorecard, write_csv


@click.command()
@click.argument("challenge_id", default="all")
@click.option("--agent", "-a", required=True, help="Agent command template. Use {task} and {workspace} as placeholders.")
@click.option("--workspace", "-w", default=None, help="Workspace directory")
@click.option("--timeout", "-t", default=300, help="Timeout per step in seconds (default: 300)")
@click.option("--summary", is_flag=True, help="Show summary with diagnostics")
@click.option("--json-output", is_flag=True, help="Output as JSON")
@click.option("--csv-output", is_flag=True, help="Output results as CSV")
@click.option("--scorecard", is_flag=True, help="Show infra scorecard (per-category breakdown)")
@click.option("--verbose", "-v", is_flag=True, help="Show full test output for each challenge")
@click.option("--parallel", "-p", default=1, help="Number of parallel workers (default: 1, sequential)")
@click.option("--no-score", is_flag=True, help="Skip scoring after run")
def run(challenge_id: str, agent: str, workspace: str | None, timeout: int,
        summary: bool, json_output: bool, csv_output: bool, scorecard: bool,
        verbose: bool, parallel: int, no_score: bool):
    """Run an agent against a challenge or all challenges.

    The agent command template uses {task} and {workspace} placeholders:

        opengym run 101 --agent "python my_agent.py --task '{task}' --dir {workspace}"

    For multi-session challenges, the agent is invoked once per session step
    with its process killed between steps to test persistent memory.
    """
    ws = Path(workspace) if workspace else get_workspace_dir()
    challenges_dir = get_challenges_dir()

    ids = resolve_challenge_ids(challenge_id, challenges_dir)
    if not ids:
        click.echo(f"Error: Challenge '{challenge_id}' not found.", err=True)
        raise SystemExit(1)

    if parallel > 1:
        results = _run_parallel(ids, challenges_dir, ws, agent, timeout, no_score, parallel)
    else:
        results = _run_sequential(ids, challenges_dir, ws, agent, timeout, no_score, verbose)

    # Output results
    if results and csv_output:
        write_csv(results)
    elif results and scorecard:
        report = build_scorecard(results)
        if json_output:
            click.echo(json.dumps(report, indent=2))
        else:
            print_scorecard(report)
    elif results and (summary or json_output):
        report = build_summary(results)
        if json_output:
            click.echo(json.dumps(report, indent=2))
        else:
            print_summary(report)
    elif results and not json_output and not csv_output:
        total = round(sum(r["score"] for r in results) / len(results))
        passed = sum(1 for r in results if r["passed"])
        click.echo(f"\n{'='*50}", err=True)
        click.echo(f"  Total: {total}/100 ({passed}/{len(results)} passed)", err=True)
        click.echo(f"{'='*50}", err=True)


def _run_sequential(ids: list[str], challenges_dir: Path, ws: Path, agent: str,
                    timeout: int, no_score: bool, verbose: bool) -> list[dict]:
    """Run challenges one at a time with progress reporting."""
    results = []
    for i, cid in enumerate(ids, 1):
        click.echo(f"\n[{i}/{len(ids)}] Running: {cid}", err=True)

        src = challenges_dir / cid
        challenge_ws = ws / cid

        # Fetch if not already present
        if not challenge_ws.exists():
            shutil.copytree(src, challenge_ws)
            click.echo(f"  Fetched to {challenge_ws}", err=True)

        # Load metadata
        meta_file = src / "metadata.yaml"
        with open(meta_file) as f:
            meta = yaml.safe_load(f)

        challenge_type = meta.get("type", "single-session")
        run_start = time.time()

        if challenge_type == "multi-session":
            run_multi_session(cid, challenge_ws, agent, meta, timeout)
        else:
            run_single_session(cid, challenge_ws, agent, meta, timeout)

        # Score
        if not no_score:
            result = score_challenge(cid, challenge_ws, src, timeout=timeout)
            # Override duration to include agent run time, not just scoring time
            result["duration_seconds"] = round(time.time() - run_start, 2)
            results.append(result)

            status = "PASS" if result["passed"] else "FAIL"
            click.echo(f"  Result: {status} ({result['tests_passed']}/{result['tests_total']} tests, score: {result['score']}/100)", err=True)

            if not result["passed"] and "failed_tests" in result:
                for ft in result["failed_tests"][:3]:
                    msg = ft.get("message", "")
                    if len(msg) > 80:
                        msg = msg[:77] + "..."
                    if msg:
                        click.echo(f"    FAIL  {ft['name']}: {msg}", err=True)
                    else:
                        click.echo(f"    FAIL  {ft['name']}", err=True)
                remaining = len(result["failed_tests"]) - 3
                if remaining > 0:
                    click.echo(f"    ... and {remaining} more failed tests", err=True)

            if verbose and "output" in result:
                click.echo(result["output"], err=True)

    return results


def _run_parallel(ids: list[str], challenges_dir: Path, ws: Path, agent: str,
                  timeout: int, no_score: bool, parallel: int) -> list[dict]:
    """Run challenges in parallel using ProcessPoolExecutor."""
    click.echo(f"\nRunning {len(ids)} challenges with {parallel} workers...\n", err=True)

    results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(
                _run_one_challenge, cid, challenges_dir, ws, agent, timeout, no_score
            ): cid
            for cid in ids
        }
        for future in as_completed(futures):
            cid = futures[future]
            completed += 1
            try:
                result = future.result()
                if result:
                    results.append(result)
                    status = "PASS" if result["passed"] else "FAIL"
                    click.echo(
                        f"  [{completed}/{len(ids)}] {cid}: {status} ({result['score']}/100)",
                        err=True,
                    )
            except Exception as exc:
                click.echo(
                    f"  [{completed}/{len(ids)}] {cid}: ERROR ({exc})",
                    err=True,
                )

    # Sort results by challenge ID for deterministic output
    results.sort(key=lambda r: r["challenge"])
    return results


def _run_one_challenge(cid: str, challenges_dir: Path, ws: Path, agent_cmd: str,
                       timeout: int, no_score: bool) -> dict | None:
    """Run and score a single challenge. Designed to be called by parallel workers."""
    src = challenges_dir / cid
    challenge_ws = ws / cid

    # Fetch if not already present
    if not challenge_ws.exists():
        shutil.copytree(src, challenge_ws)

    # Load metadata
    meta_file = src / "metadata.yaml"
    with open(meta_file) as f:
        meta = yaml.safe_load(f)

    challenge_type = meta.get("type", "single-session")
    run_start = time.time()

    if challenge_type == "multi-session":
        run_multi_session(cid, challenge_ws, agent_cmd, meta, timeout)
    else:
        run_single_session(cid, challenge_ws, agent_cmd, meta, timeout)

    if not no_score:
        result = score_challenge(cid, challenge_ws, src, timeout=timeout)
        result["duration_seconds"] = round(time.time() - run_start, 2)
        return result
    return None


def run_single_session(challenge_id: str, workspace: Path, agent_cmd: str, meta: dict, timeout: int) -> bool:
    """Run agent once for a single-session challenge."""
    # Read task from README
    readme = workspace / "README.md"
    if not readme.exists():
        click.echo(f"  Error: No README.md in {workspace}", err=True)
        return False

    task = readme.read_text(encoding="utf-8")

    # Build and run agent command
    return invoke_agent(agent_cmd, task, workspace, meta, timeout)


def run_multi_session(challenge_id: str, workspace: Path, agent_cmd: str, meta: dict, timeout: int) -> bool:
    """Run agent across multiple sessions, killing process between steps."""
    num_steps = meta.get("steps", 1)
    persist_patterns = meta.get("persist", [])
    step_timeout = meta.get("step_timeout", timeout)

    steps_dir = workspace / "steps"
    if not steps_dir.exists():
        click.echo(f"  Error: Multi-session challenge missing steps/ directory", err=True)
        return False

    for step in range(1, num_steps + 1):
        click.echo(f"\n  --- Session {step}/{num_steps} ---", err=True)

        # Read step task
        step_file = steps_dir / f"step_{step}.md"
        if not step_file.exists():
            click.echo(f"  Error: Missing {step_file.name}", err=True)
            return False

        task = step_file.read_text(encoding="utf-8")

        # Run agent for this step
        invoke_agent(agent_cmd, task, workspace, meta, step_timeout)

        # Clean workspace between steps (not after last step)
        if step < num_steps:
            cleaned = clean_workspace(workspace, persist_patterns)
            click.echo(f"  Session {step} complete. Cleaned workspace ({cleaned} files removed). Persisted: {persist_patterns}", err=True)

    click.echo(f"\n  All {num_steps} sessions complete.", err=True)
    return True


def invoke_agent(agent_cmd: str, task: str, workspace: Path, meta: dict, timeout: int) -> bool:
    """Invoke the agent command with substituted placeholders."""
    # Write task to a temp file so agents can read it (avoids shell escaping issues)
    task_file = workspace / ".opengym_task.md"
    task_file.write_text(task, encoding="utf-8")

    # Substitute placeholders
    cmd = agent_cmd.replace("{workspace}", str(workspace))
    cmd = cmd.replace("{task}", str(task_file))
    cmd = cmd.replace("{task_content}", task.replace('"', '\\"')[:2000])

    # Set up environment with tools/ on PATH
    env = os.environ.copy()
    tools_dir = workspace / "tools"
    if tools_dir.exists():
        env["PATH"] = str(tools_dir) + os.pathsep + env.get("PATH", "")
        env["OPENGYM_TOOLS_DIR"] = str(tools_dir)

    env["OPENGYM_WORKSPACE"] = str(workspace)

    click.echo(f"  Invoking agent (timeout: {timeout}s)...", err=True)

    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=str(workspace),
            timeout=timeout,
            env=env,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            click.echo(f"  Agent exited with code {proc.returncode}", err=True)
            if proc.stderr:
                click.echo(f"  Agent stderr: {proc.stderr[-300:]}", err=True)
        return proc.returncode == 0
    except subprocess.TimeoutExpired:
        click.echo(f"  Agent timed out after {timeout}s. Try --timeout {timeout * 2} for complex challenges.", err=True)
        return False
    finally:
        # Clean up task file
        if task_file.exists():
            task_file.unlink()


def clean_workspace(workspace: Path, persist_patterns: list[str]) -> int:
    """Remove non-persisted files from setup/ between sessions.

    Protected directories (tests/, steps/, tools/) are never cleaned.
    Only files in setup/ are subject to cleanup.
    """
    setup_dir = workspace / "setup"
    if not setup_dir.exists():
        return 0

    removed = 0

    for item in list(setup_dir.rglob("*")):
        if not item.exists() or not item.is_file():
            continue

        relative = str(item.relative_to(workspace)).replace("\\", "/")

        # Check if file matches any persist pattern
        should_persist = any(fnmatch(relative, p) for p in persist_patterns)

        if not should_persist:
            item.unlink()
            removed += 1

    # Clean up empty directories in setup/
    for dirpath in sorted(setup_dir.rglob("*"), reverse=True):
        if dirpath.is_dir() and not any(dirpath.iterdir()):
            dirpath.rmdir()

    return removed
