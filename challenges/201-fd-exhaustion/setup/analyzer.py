"""Log analyzer — BUG: opens all files simultaneously, exhausting file descriptors.
Rewrite to use at most 5 concurrent file descriptors."""

import os
import glob

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

def analyze_logs():
    """BAD: opens all log files at once and keeps them open."""
    log_dir = os.path.join(SETUP_DIR, "logs")
    log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")))

    # BUG: opens ALL files and keeps handles in a list
    open_handles = []
    for fpath in log_files:
        fh = open(fpath, 'r')
        open_handles.append(fh)

    total_lines = 0
    error_count = 0
    warning_count = 0

    # Reads from all open handles
    for fh in open_handles:
        for line in fh:
            total_lines += 1
            if "ERROR" in line:
                error_count += 1
            if "WARNING" in line:
                warning_count += 1

    # Never closes handles — FD leak
    result = {
        "total_lines": total_lines,
        "error_count": error_count,
        "warning_count": warning_count,
        "files_processed": len(log_files),
        "max_concurrent_fds": len(log_files)
    }
    return result

if __name__ == "__main__":
    import json
    result = analyze_logs()
    with open(os.path.join(SETUP_DIR, "analysis.json"), "w") as f:
        json.dump(result, f, indent=2)
