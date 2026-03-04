#!/usr/bin/env python3
"""OpenClaw agent adapter for OpenGym challenges.

This adapter runs tasks through OpenClaw with full infrastructure:
- Memory persistence (MEMORY.md, memory/*.md)
- Tool access (exec, read, write, edit)
- Full agent capabilities

Usage:
    opengym run 101 --agent "python examples/agents/openclaw_agent.py --task '{task}' --dir {workspace}"

Requires:
    - OpenClaw installed (`pip install openclaw` or from source)
    - For --local: model provider API keys in environment
    - For gateway mode: running gateway (`openclaw gateway start`)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_openclaw_task(task: str, workspace: Path, timeout: int = 300, local: bool = True) -> bool:
    """Run task through OpenClaw agent command."""
    
    # Build the prompt with workspace context
    prompt = f"""You are solving an OpenGym challenge.

WORKSPACE: {workspace}

IMPORTANT RULES:
1. All file operations must be relative to the workspace: {workspace}
2. Read files before modifying them
3. Only modify files within the workspace
4. When the task is complete, ensure all required output files exist

TASK:
{task}

Begin working on the task now. Use tools to read, write, and execute commands as needed.
"""
    
    # Use openclaw agent command
    cmd = [
        "openclaw", "agent",
        "--message", prompt,
        "--timeout", str(timeout),
        "--json",
    ]
    
    if local:
        cmd.append("--local")
    
    # Set working directory
    env = os.environ.copy()
    env["OPENGYM_WORKSPACE"] = str(workspace)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 60,  # Extra buffer
            cwd=str(workspace),
            env=env,
        )
        
        if result.returncode == 0:
            print(f"OpenClaw completed successfully", file=sys.stderr)
            # Check if output contains success indicators
            if "error" not in result.stdout.lower() or "completed" in result.stdout.lower():
                return True
        
        print(f"OpenClaw output: {result.stdout[-500:]}", file=sys.stderr)
        if result.stderr:
            print(f"OpenClaw stderr: {result.stderr[-300:]}", file=sys.stderr)
        return result.returncode == 0
            
    except subprocess.TimeoutExpired:
        print(f"OpenClaw timed out after {timeout}s", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'openclaw' command not found. Is OpenClaw installed?", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="OpenClaw agent for OpenGym")
    parser.add_argument("--task", "-t", required=True, help="Path to task file")
    parser.add_argument("--dir", "-d", required=True, help="Workspace directory")
    parser.add_argument("--timeout", default=300, type=int, help="Timeout in seconds")
    parser.add_argument("--gateway", action="store_true", help="Use gateway instead of local mode")
    args = parser.parse_args()
    
    # Read task from file
    task_path = Path(args.task)
    if not task_path.exists():
        print(f"Error: Task file not found: {task_path}", file=sys.stderr)
        sys.exit(1)
    
    task = task_path.read_text(encoding="utf-8")
    workspace = Path(args.dir).resolve()
    
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)
    
    print(f"OpenClaw agent starting...", file=sys.stderr)
    print(f"  Workspace: {workspace}", file=sys.stderr)
    print(f"  Mode: {'gateway' if args.gateway else 'local'}", file=sys.stderr)
    print(f"  Timeout: {args.timeout}s", file=sys.stderr)
    
    success = run_openclaw_task(task, workspace, args.timeout, local=not args.gateway)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
