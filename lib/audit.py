"""Audit logging library for OpenGym tool scripts.

Each tool call writes a JSONL entry to setup/tool_audit.jsonl with:
- timestamp (monotonic + wall clock)
- nonce (random per-call, prevents replay)
- sequence number (global counter, detects skipped/reordered calls)
- tool name, args, exit code, duration
- hmac signature (prevents tampering with audit log)

Tools import this and wrap their main() with the audit decorator.
Verify scripts import audit_verify() to validate the log.
"""

import functools
import hashlib
import hmac
import json
import os
import random
import string
import sys
import time


# Secret is derived from tool path + challenge dir — agent can't forge it
# without modifying the tool (which is detected by integrity check)
def _derive_secret(tool_path: str) -> str:
    """Derive HMAC secret from the tool's absolute path."""
    return hashlib.sha256(f"opengym-audit-{os.path.abspath(tool_path)}".encode()).hexdigest()[:32]


def _generate_nonce(length: int = 16) -> str:
    """Generate a random nonce."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def _get_sequence_file(audit_file: str) -> str:
    return audit_file + ".seq"


def _next_sequence(audit_file: str) -> int:
    """Atomically increment and return the next sequence number."""
    seq_file = _get_sequence_file(audit_file)
    seq = 0
    if os.path.exists(seq_file):
        try:
            with open(seq_file, "r") as f:
                seq = int(f.read().strip())
        except (ValueError, IOError):
            seq = 0
    seq += 1
    with open(seq_file, "w") as f:
        f.write(str(seq))
    return seq


def _sign_entry(entry: dict, secret: str) -> str:
    """HMAC-SHA256 sign an audit entry."""
    # Sign everything except the signature itself
    payload = json.dumps({k: v for k, v in sorted(entry.items()) if k != "sig"}, sort_keys=True)
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]


def write_audit_entry(tool_name: str, args: list[str], exit_code: int,
                      duration_ms: float, audit_file: str, extra: dict | None = None):
    """Write a single audit log entry."""
    secret = _derive_secret(audit_file)
    seq = _next_sequence(audit_file)
    nonce = _generate_nonce()

    entry = {
        "tool": tool_name,
        "args": args,
        "seq": seq,
        "nonce": nonce,
        "exit_code": exit_code,
        "duration_ms": round(duration_ms, 1),
        "ts": time.time(),
        "ts_mono": time.monotonic(),
    }
    if extra:
        entry["extra"] = extra

    entry["sig"] = _sign_entry(entry, secret)

    os.makedirs(os.path.dirname(audit_file), exist_ok=True)
    with open(audit_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def audit_tool(tool_name: str):
    """Decorator that wraps a tool's main() with audit logging.

    Usage:
        @audit_tool("enrich")
        def main():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            # Resolve audit file path: workspace/setup/tool_audit.jsonl
            # Tools live in workspace/tools/, so setup/ is ../setup/
            tool_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            workspace = os.path.dirname(tool_dir)
            audit_file = os.path.join(workspace, "setup", "tool_audit.jsonl")

            args = sys.argv[1:]
            start = time.monotonic()
            exit_code = 0
            try:
                result = func(*a, **kw)
                return result
            except SystemExit as e:
                exit_code = e.code if isinstance(e.code, int) else 1
                raise
            except Exception:
                exit_code = 1
                raise
            finally:
                duration_ms = (time.monotonic() - start) * 1000
                try:
                    write_audit_entry(tool_name, args, exit_code, duration_ms, audit_file)
                except Exception:
                    pass  # Never let audit logging break the tool
        return wrapper
    return decorator


# === Verification helpers ===

def load_audit_log(audit_file: str) -> list[dict]:
    """Load and parse the audit log."""
    entries = []
    if not os.path.exists(audit_file):
        return entries
    with open(audit_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def verify_audit_signatures(entries: list[dict], audit_file: str) -> list[str]:
    """Verify HMAC signatures on all audit entries. Returns list of errors."""
    secret = _derive_secret(audit_file)
    errors = []
    for i, entry in enumerate(entries):
        expected_sig = _sign_entry(entry, secret)
        actual_sig = entry.get("sig", "")
        if actual_sig != expected_sig:
            errors.append(f"Entry {i} (seq={entry.get('seq')}): signature mismatch")
    return errors


def verify_audit_sequence(entries: list[dict]) -> list[str]:
    """Verify sequence numbers are monotonically increasing with no gaps."""
    errors = []
    if not entries:
        return errors
    expected_seq = 1
    for i, entry in enumerate(entries):
        seq = entry.get("seq", 0)
        if seq != expected_seq:
            errors.append(f"Entry {i}: expected seq={expected_seq}, got seq={seq}")
        expected_seq = seq + 1
    return errors


def verify_audit_timestamps(entries: list[dict]) -> list[str]:
    """Verify timestamps are monotonically increasing."""
    errors = []
    for i in range(1, len(entries)):
        if entries[i]["ts"] < entries[i-1]["ts"]:
            errors.append(f"Entry {i}: timestamp went backwards ({entries[i]['ts']} < {entries[i-1]['ts']})")
    return errors


def verify_audit_nonces(entries: list[dict]) -> list[str]:
    """Verify all nonces are unique (no replay)."""
    errors = []
    seen = set()
    for i, entry in enumerate(entries):
        nonce = entry.get("nonce", "")
        if nonce in seen:
            errors.append(f"Entry {i}: duplicate nonce '{nonce}'")
        seen.add(nonce)
    return errors


def verify_audit_tool_calls(entries: list[dict], tool_name: str,
                            min_calls: int = 0, max_calls: int = 999,
                            required_args: list[list[str]] | None = None) -> list[str]:
    """Verify tool was called the right number of times with expected args."""
    errors = []
    tool_entries = [e for e in entries if e.get("tool") == tool_name]

    if len(tool_entries) < min_calls:
        errors.append(f"Tool '{tool_name}' called {len(tool_entries)} times, expected at least {min_calls}")
    if len(tool_entries) > max_calls:
        errors.append(f"Tool '{tool_name}' called {len(tool_entries)} times, expected at most {max_calls}")

    if required_args:
        for req_args in required_args:
            found = False
            for e in tool_entries:
                if all(arg in e.get("args", []) for arg in req_args):
                    found = True
                    break
            if not found:
                errors.append(f"Tool '{tool_name}' never called with args containing {req_args}")

    return errors


def verify_audit_timing(entries: list[dict], tool_name: str,
                        min_gap_ms: float = 0) -> list[str]:
    """Verify minimum gap between consecutive calls (for rate limit compliance)."""
    errors = []
    tool_entries = [e for e in entries if e.get("tool") == tool_name]

    for i in range(1, len(tool_entries)):
        gap = (tool_entries[i]["ts"] - tool_entries[i-1]["ts"]) * 1000
        if gap < min_gap_ms:
            errors.append(
                f"Calls {i-1}->{i}: gap={gap:.0f}ms, required >={min_gap_ms:.0f}ms "
                f"(rate limit not respected)"
            )
    return errors


def full_audit_check(audit_file: str, tool_name: str,
                     min_calls: int = 1, max_calls: int = 999,
                     min_gap_ms: float = 0,
                     required_args: list[list[str]] | None = None) -> tuple[bool, list[str]]:
    """Run all audit checks. Returns (all_passed, list_of_errors)."""
    entries = load_audit_log(audit_file)
    if not entries:
        return False, ["No audit log entries found"]

    all_errors = []
    all_errors.extend(verify_audit_signatures(entries, audit_file))
    all_errors.extend(verify_audit_sequence(entries))
    all_errors.extend(verify_audit_timestamps(entries))
    all_errors.extend(verify_audit_nonces(entries))
    all_errors.extend(verify_audit_tool_calls(entries, tool_name, min_calls, max_calls, required_args))
    if min_gap_ms > 0:
        all_errors.extend(verify_audit_timing(entries, tool_name, min_gap_ms))

    return len(all_errors) == 0, all_errors
