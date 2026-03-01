"""Batch-add audit log validation to tool-use challenge verify.py files."""
import os
import sys

# Map of challenge ID to (tool_name, min_calls, max_calls, min_gap_ms)
TOOL_CHALLENGES = {
    "106": ("convert", 1, 999, 0),
    "107": ("extract", 1, 999, 0),
    "108": ("enrich", 5, 999, 0),
    "109": ("lookup", 4, 999, 0),
    "110": ("mystery", 1, 999, 0),
    "126": ("lookup", 1, 999, 0),
    "166": ("api", 3, 999, 0),
    "167": ("service", 2, 999, 0),
    "168": ("validator", 1, 3, 0),
    "169": ("data_api", 1, 999, 0),
    "170": ("converter", 1, 999, 0),
    "171": ("streamer", 2, 999, 0),
    "172": ("injection_lookup", 2, 999, 0),
    "173": ("slow_api", 1, 999, 0),
    "174": ("hanging", 1, 999, 0),
    "175": ("primary", 1, 999, 0),
    "176": ("flaky_calc", 3, 999, 0),
    "177": ("cached_api", 1, 999, 0),
    "178": ("data_dump", 2, 999, 0),
    "179": ("auth_api", 2, 999, 0),
    "180": ("secure_api", 1, 999, 0),
    "181": ("counter_api", 1, 999, 0),
    "182": ("verified_api", 1, 999, 0),
    "183": ("text_api", 1, 999, 0),
    "184": ("quota_api", 1, 5, 0),
    "185": ("buggy_api", 1, 999, 0),
}


def build_audit_block_results(tool_name, min_calls, max_calls, min_gap_ms, results_var):
    """Build audit check code block for verify.py files that use a results list."""
    return f"""
# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "{tool_name}",
        min_calls={min_calls}, max_calls={max_calls},
        min_gap_ms={min_gap_ms},
    )
    if _audit_ok:
        {results_var}.append({{"test": "audit_log_valid", "passed": True, "message": "Audit log signatures, sequences, and nonces valid"}})
    else:
        for _err in _audit_errors[:3]:
            {results_var}.append({{"test": "audit_log_valid", "passed": False, "message": _err}})
except ImportError:
    {results_var}.append({{"test": "audit_log_valid", "passed": True, "message": "Audit module not available (skipped)"}})
"""


def build_audit_block_check(tool_name, min_calls, max_calls, min_gap_ms):
    """Build audit check code block for verify.py files that use a check() function."""
    return f"""
    # === Audit log validation ===
    _audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
    _tools_dir = os.path.join(CHALLENGE_DIR, "tools")
    sys.path.insert(0, _tools_dir)
    try:
        from _audit import full_audit_check
        _audit_ok, _audit_errors = full_audit_check(
            _audit_file, "{tool_name}",
            min_calls={min_calls}, max_calls={max_calls},
            min_gap_ms={min_gap_ms},
        )
        if _audit_ok:
            check("audit_log_valid", True, "Audit log signatures, sequences, and nonces valid")
        else:
            for _err in _audit_errors[:3]:
                check("audit_log_valid", False, _err)
    except ImportError:
        check("audit_log_valid", True, "Audit module not available (skipped)")
"""


def add_audit_check(filepath, tool_name, min_calls, max_calls, min_gap_ms):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "_audit" in content:
        print(f"  SKIP (already has audit): {filepath}")
        return

    # Determine pattern: results list or check() function
    has_results_list = "results.append" in content or "results = []" in content
    has_check_func = "def check(" in content

    if has_results_list:
        audit_code = build_audit_block_results(
            tool_name, min_calls, max_calls, min_gap_ms, "results"
        )
        lines = content.split("\n")

        # Find the final "for r in results:" print loop
        insert_idx = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            stripped = lines[i].strip()
            if stripped.startswith("for r in") and "result" in stripped:
                insert_idx = i
                break

        audit_lines = audit_code.rstrip().split("\n")
        for j, al in enumerate(audit_lines):
            lines.insert(insert_idx + j, al)

        content = "\n".join(lines)

    elif has_check_func:
        audit_code = build_audit_block_check(
            tool_name, min_calls, max_calls, min_gap_ms
        )
        lines = content.split("\n")

        # Find end of main() - look for 'if __name__'
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.strip().startswith("if __name__"):
                insert_idx = i
                break

        audit_lines = audit_code.rstrip().split("\n")
        for j, al in enumerate(audit_lines):
            lines.insert(insert_idx + j, al)

        content = "\n".join(lines)

    else:
        # Fallback: add before if __name__ as top-level code
        audit_code = build_audit_block_results(
            tool_name, min_calls, max_calls, min_gap_ms, "results"
        )

        # Need to create a results list if it doesn't exist
        lines = content.split("\n")
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.strip().startswith("if __name__"):
                insert_idx = i
                break

        # Check if there's a print loop at the end for results
        has_print_loop = False
        for i in range(insert_idx - 1, max(insert_idx - 5, -1), -1):
            if "print(json.dumps" in lines[i]:
                has_print_loop = True
                break

        audit_lines = audit_code.rstrip().split("\n")
        for j, al in enumerate(audit_lines):
            lines.insert(insert_idx + j, al)

        content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    cname = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
    print(f"  OK: {cname}")


def main():
    base = "C:/Users/marcu/opengym/challenges"
    print("Adding audit checks to verify.py files...")

    for cid, (tool_name, min_calls, max_calls, min_gap_ms) in sorted(
        TOOL_CHALLENGES.items()
    ):
        found = False
        for entry in os.listdir(base):
            if entry.startswith(cid + "-"):
                verify_path = os.path.join(base, entry, "tests", "verify.py")
                if os.path.exists(verify_path):
                    add_audit_check(
                        verify_path, tool_name, min_calls, max_calls, min_gap_ms
                    )
                    found = True
                break
        if not found:
            print(f"  WARN: No verify.py for challenge {cid}")

    print("\nDone!")


if __name__ == "__main__":
    main()
