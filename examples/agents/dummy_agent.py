#!/usr/bin/env python3
"""Dummy agent for testing the OpenGym pipeline. Does not solve anything."""

import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="OpenGym Dummy Agent")
    parser.add_argument("--task", required=True, help="Path to task file")
    parser.add_argument("--dir", required=True, help="Workspace directory")
    args = parser.parse_args()

    task_path = Path(args.task)
    workspace = Path(args.dir)

    if not task_path.exists():
        print(f"[dummy] Error: Task file not found: {task_path}", file=sys.stderr)
        sys.exit(1)
    if not workspace.is_dir():
        print(f"[dummy] Error: Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    task_content = task_path.read_text(encoding="utf-8")
    print(f"[dummy] Workspace: {workspace}")
    print(f"[dummy] Task file: {task_path}")
    print(f"[dummy] Task length: {len(task_content)} chars")
    print(f"[dummy] Task preview: {task_content[:200]}...")

    setup_dir = workspace / "setup"
    if setup_dir.exists():
        files = [f for f in setup_dir.rglob("*") if f.is_file()]
        print(f"[dummy] setup/ contains {len(files)} file(s):")
        for f in files[:10]:
            print(f"  {f.relative_to(workspace)}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")

    print(f"[dummy] OPENGYM_WORKSPACE={os.environ.get('OPENGYM_WORKSPACE', '(not set)')}")
    print(f"[dummy] OPENGYM_TOOLS_DIR={os.environ.get('OPENGYM_TOOLS_DIR', '(not set)')}")

    tools_dir = workspace / "tools"
    if tools_dir.exists():
        tools = [f.name for f in tools_dir.iterdir() if f.is_file() and f.suffix == ".py"]
        print(f"[dummy] Available tools: {tools}")

    print("[dummy] Done. (No changes made)")


if __name__ == "__main__":
    main()
