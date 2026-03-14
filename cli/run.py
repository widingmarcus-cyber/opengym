"""Run an agent against challenges with multi-session orchestration."""

import hashlib
import json
import os
import shutil
import signal
import subprocess
import threading
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from fnmatch import fnmatch
from pathlib import Path

import click
import yaml

from cli.score import (
    build_scorecard,
    build_summary,
    print_scorecard,
    print_summary,
    score_challenge,
    write_csv,
)
from cli.utils import get_challenges_dir, get_workspace_dir, resolve_challenge_ids

ALLOWED_MUTATION_PREFIXES = (
    "setup/",
    "tools/.state/",
)
ALLOWED_MUTATION_FILES = {
    ".opengym_task.md",
    "tools/_audit.py",
}


@click.command()
@click.argument("challenge_id", default="all")
@click.option(
    "--agent",
    "-a",
    required=True,
    help="Agent command template. Use {task}, {workspace}, and optional {repo} placeholders.",
)
@click.option("--workspace", "-w", default=None, help="Workspace directory")
@click.option(
    "--timeout", "-t", default=300, help="Timeout per step in seconds (default: 300)"
)
@click.option("--summary", is_flag=True, help="Show summary with diagnostics")
@click.option("--json-output", is_flag=True, help="Output as JSON")
@click.option("--csv-output", is_flag=True, help="Output results as CSV")
@click.option(
    "--scorecard", is_flag=True, help="Show infra scorecard (per-category breakdown)"
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Show full test output for each challenge"
)
@click.option(
    "--parallel",
    "-p",
    default=1,
    help="Number of parallel workers (default: 1, sequential)",
)
@click.option("--no-score", is_flag=True, help="Skip scoring after run")
@click.option(
    "--enforce-scope/--no-enforce-scope",
    default=True,
    help="Fail run if agent modifies files outside setup/ (except tools/.state).",
)
def run(
    challenge_id: str,
    agent: str,
    workspace: str | None,
    timeout: int,
    summary: bool,
    json_output: bool,
    csv_output: bool,
    scorecard: bool,
    verbose: bool,
    parallel: int,
    no_score: bool,
    enforce_scope: bool,
):
    """Run an agent against a challenge or all challenges.

    The agent command template uses {task}, {workspace}, and {repo} placeholders:

        opengym run 101 --agent "python {repo}/my_agent.py --task '{task}' --dir {workspace}"

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
        results = _run_parallel(
            ids, challenges_dir, ws, agent, timeout, no_score, parallel, enforce_scope
        )
    else:
        results = _run_sequential(
            ids, challenges_dir, ws, agent, timeout, no_score, verbose, enforce_scope
        )

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
        click.echo(f"\n{'=' * 50}", err=True)
        click.echo(f"  Total: {total}/100 ({passed}/{len(results)} passed)", err=True)
        click.echo(f"{'=' * 50}", err=True)


def _run_sequential(
    ids: list[str],
    challenges_dir: Path,
    ws: Path,
    agent: str,
    timeout: int,
    no_score: bool,
    verbose: bool,
    enforce_scope: bool,
) -> list[dict]:
    """Run challenges one at a time with progress reporting."""
    results = []
    for i, cid in enumerate(ids, 1):
        click.echo(f"\n[{i}/{len(ids)}] Running: {cid}", err=True)

        src = challenges_dir / cid
        challenge_ws = ws / cid

        # Fetch if not already present (exclude tests/steps to prevent answer leakage)
        if not challenge_ws.exists():
            shutil.copytree(
                src, challenge_ws, ignore=shutil.ignore_patterns("tests", "steps")
            )
            click.echo(f"  Fetched to {challenge_ws}", err=True)

        # Load metadata
        meta_file = src / "metadata.yaml"
        with open(meta_file) as f:
            meta = yaml.safe_load(f)

        challenge_type = meta.get("type", "single-session")
        run_start = time.time()

        if challenge_type == "multi-session":
            run_multi_session(
                cid,
                challenge_ws,
                agent,
                meta,
                timeout,
                original_path=src,
                enforce_scope=enforce_scope,
            )
        else:
            run_single_session(
                cid, challenge_ws, agent, meta, timeout, enforce_scope=enforce_scope
            )

        # Score
        if not no_score:
            result = score_challenge(
                cid, challenge_ws, src, timeout=timeout, _internal=True
            )
            # Override duration to include agent run time, not just scoring time
            result["duration_seconds"] = round(time.time() - run_start, 2)
            results.append(result)

            status = "PASS" if result["passed"] else "FAIL"
            click.echo(
                f"  Result: {status} ({result['tests_passed']}/{result['tests_total']} tests, score: {result['score']}/100)",
                err=True,
            )

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


def _run_parallel(
    ids: list[str],
    challenges_dir: Path,
    ws: Path,
    agent: str,
    timeout: int,
    no_score: bool,
    parallel: int,
    enforce_scope: bool,
) -> list[dict]:
    """Run challenges in parallel using ProcessPoolExecutor."""
    click.echo(
        f"\nRunning {len(ids)} challenges with {parallel} workers...\n", err=True
    )

    results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(
                _run_one_challenge,
                cid,
                challenges_dir,
                ws,
                agent,
                timeout,
                no_score,
                enforce_scope,
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


def _run_one_challenge(
    cid: str,
    challenges_dir: Path,
    ws: Path,
    agent_cmd: str,
    timeout: int,
    no_score: bool,
    enforce_scope: bool,
) -> dict | None:
    """Run and score a single challenge. Designed to be called by parallel workers."""
    src = challenges_dir / cid
    challenge_ws = ws / cid

    # Fetch if not already present (exclude tests/steps to prevent answer leakage)
    if not challenge_ws.exists():
        shutil.copytree(
            src, challenge_ws, ignore=shutil.ignore_patterns("tests", "steps")
        )

    # Load metadata
    meta_file = src / "metadata.yaml"
    with open(meta_file) as f:
        meta = yaml.safe_load(f)

    challenge_type = meta.get("type", "single-session")
    run_start = time.time()

    if challenge_type == "multi-session":
        run_multi_session(
            cid,
            challenge_ws,
            agent_cmd,
            meta,
            timeout,
            original_path=src,
            enforce_scope=enforce_scope,
        )
    else:
        run_single_session(
            cid, challenge_ws, agent_cmd, meta, timeout, enforce_scope=enforce_scope
        )

    if not no_score:
        result = score_challenge(
            cid, challenge_ws, src, timeout=timeout, _internal=True
        )
        result["duration_seconds"] = round(time.time() - run_start, 2)
        return result
    return None


def run_single_session(
    challenge_id: str,
    workspace: Path,
    agent_cmd: str,
    meta: dict,
    timeout: int,
    enforce_scope: bool = True,
) -> bool:
    """Run agent once for a single-session challenge."""
    # Read task from README
    readme = workspace / "README.md"
    if not readme.exists():
        click.echo(f"  Error: No README.md in {workspace}", err=True)
        return False

    task = readme.read_text(encoding="utf-8")

    # Build and run agent command
    return invoke_agent(
        agent_cmd,
        task,
        workspace,
        meta,
        timeout,
        step=1,
        enforce_scope=enforce_scope,
    )


def run_multi_session(
    challenge_id: str,
    workspace: Path,
    agent_cmd: str,
    meta: dict,
    timeout: int,
    original_path: Path = None,
    enforce_scope: bool = True,
) -> bool:
    """Run agent across multiple sessions, killing process between steps."""
    num_steps = meta.get("steps", 1)
    persist_patterns = meta.get("persist", [])
    step_timeout = meta.get("step_timeout", timeout)

    # Read steps from original challenge path (not workspace) to prevent agent
    # from browsing future step files
    steps_dir = original_path / "steps" if original_path else workspace / "steps"
    if not steps_dir.exists():
        click.echo(
            f"  Error: Multi-session challenge missing steps/ directory", err=True
        )
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
        invoke_agent(
            agent_cmd,
            task,
            workspace,
            meta,
            step_timeout,
            step=step,
            enforce_scope=enforce_scope,
        )

        # Clean workspace between steps (not after last step)
        if step < num_steps:
            cleaned = clean_workspace(workspace, persist_patterns)
            click.echo(
                f"  Session {step} complete. Cleaned workspace ({cleaned} files removed). Persisted: {persist_patterns}",
                err=True,
            )

    click.echo(f"\n  All {num_steps} sessions complete.", err=True)
    return True


def invoke_agent(
    agent_cmd: str,
    task: str,
    workspace: Path,
    meta: dict,
    timeout: int,
    step: int | None = None,
    enforce_scope: bool = True,
) -> bool:
    """Invoke the agent command with substituted placeholders."""
    before_snapshot = _snapshot_workspace(workspace) if enforce_scope else {}

    # Write task to a temp file so agents can read it (avoids shell escaping issues)
    task_file = workspace / ".opengym_task.md"
    task_file.write_text(task, encoding="utf-8")

    # Substitute placeholders
    repo_root = Path(__file__).resolve().parent.parent
    cmd = agent_cmd
    cmd = _replace_placeholder(cmd, "workspace", str(workspace))
    cmd = _replace_placeholder(cmd, "task", str(task_file))
    cmd = _replace_placeholder(cmd, "repo", str(repo_root))
    cmd = _replace_placeholder(cmd, "task_content", task.replace('"', '\\"')[:2000])

    # Set up environment with tools/ on PATH
    env = os.environ.copy()
    tools_dir = workspace / "tools"
    injected_audit_file = None
    if tools_dir.exists():
        env["PATH"] = str(tools_dir) + os.pathsep + env.get("PATH", "")
        env["OPENGYM_TOOLS_DIR"] = str(tools_dir)

        # Inject audit module into tools directory
        audit_src = Path(__file__).resolve().parent.parent / "lib" / "audit.py"
        if audit_src.exists():
            injected_audit_file = tools_dir / "_audit.py"
            shutil.copy2(str(audit_src), str(injected_audit_file))

    env["OPENGYM_WORKSPACE"] = str(workspace)
    env["OPENGYM_REPO"] = str(repo_root)

    # Check for fault injection config
    faults = _faults_for_step(meta.get("fault_injection", []), step)

    click.echo(f"  Invoking agent (timeout: {timeout}s)...", err=True)

    run_start = time.time()
    try:
        ok = False
        if faults:
            ok = _run_with_faults(cmd, workspace, env, timeout, faults)
        else:
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
            ok = proc.returncode == 0

        if enforce_scope:
            after_snapshot = _snapshot_workspace(workspace)
            violations = _detect_scope_violations(before_snapshot, after_snapshot)
            if violations:
                click.echo(
                    "  Scope violation: modified files outside setup/ or tools/.state/",
                    err=True,
                )
                for path in violations[:5]:
                    click.echo(f"    - {path}", err=True)
                if len(violations) > 5:
                    click.echo(f"    ... and {len(violations) - 5} more", err=True)
                ok = False

        return ok
    except subprocess.TimeoutExpired:
        click.echo(
            f"  Agent timed out after {timeout}s. Try --timeout {timeout * 2} for complex challenges.",
            err=True,
        )
        return False
    finally:
        # Write behavioral log entry
        duration_s = time.time() - run_start
        _write_behavior_log(workspace, duration_s)
        # Clean up task file
        if task_file.exists():
            task_file.unlink()
        if injected_audit_file and injected_audit_file.exists():
            try:
                injected_audit_file.unlink()
            except OSError:
                pass


def _run_with_faults(
    cmd: str, workspace: Path, env: dict, timeout: int, faults: list[dict]
) -> bool:
    """Run agent with fault injection — uses Popen for mid-execution faults.

    Supported fault types:
      - file_delete: Delete a file after delay_seconds
      - file_corrupt: Corrupt a file after delay_seconds
      - file_appear: Create a file after delay_seconds
      - sigterm: Send SIGTERM after delay_seconds
      - env_change: Write a new env file after delay_seconds
    """
    proc = subprocess.Popen(
        cmd,
        shell=True,
        cwd=str(workspace),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Schedule fault injections on background threads
    for fault in faults:
        fault_type = fault.get("type", "")
        delay = fault.get("delay_seconds", 3)
        target = fault.get("target", "")

        if fault_type == "file_delete":
            threading.Thread(
                target=_fault_file_delete,
                args=(workspace / target, delay),
                daemon=True,
            ).start()
        elif fault_type == "file_corrupt":
            threading.Thread(
                target=_fault_file_corrupt,
                args=(workspace / target, delay, fault.get("content", "CORRUPTED")),
                daemon=True,
            ).start()
        elif fault_type == "file_appear":
            threading.Thread(
                target=_fault_file_appear,
                args=(workspace / target, delay, fault.get("content", "")),
                daemon=True,
            ).start()
        elif fault_type == "sigterm":
            threading.Thread(
                target=_fault_sigterm,
                args=(proc, delay),
                daemon=True,
            ).start()

    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        click.echo(f"  Agent timed out after {timeout}s.", err=True)
        return False

    if proc.returncode != 0:
        click.echo(f"  Agent exited with code {proc.returncode}", err=True)
        if stderr:
            click.echo(f"  Agent stderr: {stderr[-300:]}", err=True)
    return proc.returncode == 0


def _faults_for_step(raw_faults, step: int | None) -> list[dict]:
    """Return only fault injections that apply to this execution step."""
    if isinstance(raw_faults, dict):
        raw_faults = [raw_faults]
    if not isinstance(raw_faults, list):
        return []

    selected: list[dict] = []
    for fault in raw_faults:
        if not isinstance(fault, dict):
            continue
        fault_step = fault.get("step")
        if fault_step is None:
            selected.append(fault)
            continue
        try:
            if int(fault_step) == step:
                selected.append(fault)
        except (TypeError, ValueError):
            continue
    return selected


def _replace_placeholder(command: str, key: str, value: str) -> str:
    """Replace placeholders and normalize quoted variants for shell safety."""
    command = command.replace(f"'{{{key}}}'", f'"{value}"')
    command = command.replace(f'"{{{key}}}"', f'"{value}"')
    command = command.replace(f"{{{key}}}", value)
    return command


def _snapshot_workspace(workspace: Path) -> dict[str, str]:
    """Hash all workspace files for change-scope enforcement."""
    snapshot: dict[str, str] = {}
    if not workspace.exists():
        return snapshot

    for item in workspace.rglob("*"):
        if not item.is_file():
            continue
        rel = str(item.relative_to(workspace)).replace("\\", "/")
        try:
            digest = hashlib.sha256(item.read_bytes()).hexdigest()
        except OSError:
            continue
        snapshot[rel] = digest
    return snapshot


def _is_allowed_mutation(relative_path: str) -> bool:
    """Return True if a changed file path is allowed to mutate."""
    if relative_path in ALLOWED_MUTATION_FILES:
        return True
    return any(relative_path.startswith(prefix) for prefix in ALLOWED_MUTATION_PREFIXES)


def _detect_scope_violations(
    before: dict[str, str], after: dict[str, str]
) -> list[str]:
    """Return changed file paths outside permitted mutation scope."""
    violations = []
    for path in sorted(set(before) | set(after)):
        if before.get(path) == after.get(path):
            continue
        if not _is_allowed_mutation(path):
            violations.append(path)
    return violations


def _fault_file_delete(target: Path, delay: float):
    """Delete a file after delay."""
    time.sleep(delay)
    try:
        if target.exists():
            target.unlink()
    except Exception:
        pass


def _fault_file_corrupt(target: Path, delay: float, content: str):
    """Overwrite a file with corrupt content after delay."""
    time.sleep(delay)
    try:
        target.write_text(content, encoding="utf-8")
    except Exception:
        pass


def _fault_file_appear(target: Path, delay: float, content: str):
    """Create a file after delay (simulates late-arriving data)."""
    time.sleep(delay)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except Exception:
        pass


def _fault_sigterm(proc: subprocess.Popen, delay: float):
    """Send SIGTERM to process after delay."""
    time.sleep(delay)
    try:
        if proc.poll() is None:
            if os.name == "nt":
                proc.terminate()
            else:
                proc.send_signal(signal.SIGTERM)
    except Exception:
        pass


def _write_behavior_log(workspace: Path, duration_s: float):
    """Write a behavioral log entry to setup/behavior.jsonl."""
    setup_dir = workspace / "setup"
    setup_dir.mkdir(parents=True, exist_ok=True)
    log_file = setup_dir / "behavior.jsonl"

    entry = {
        "ts": time.time(),
        "duration_s": round(duration_s, 2),
    }

    # Check if audit log exists for tool-use challenges
    tools_dir = workspace / "tools"
    if tools_dir.exists():
        audit_file = setup_dir / "tool_audit.jsonl"
        entry["has_audit_log"] = audit_file.exists()
        if audit_file.exists():
            try:
                entry["audit_entries"] = sum(1 for _ in open(audit_file))
            except Exception:
                entry["audit_entries"] = 0

    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


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
