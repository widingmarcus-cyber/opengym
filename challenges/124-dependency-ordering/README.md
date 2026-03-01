# Challenge 124: Dependency Ordering

## Difficulty: Medium
## Category: Task Sequencing
## Dimension: Planning

## Description

You are given 8 build tasks defined in `setup/build_tasks.json`. Each task produces an output file in `setup/outputs/`. Some tasks depend on outputs from other tasks, forming a directed acyclic graph (DAG).

Your job is to:

1. Read and understand the dependency graph
2. Determine a valid execution order (topological sort)
3. Execute each task in order, creating the output files
4. Write a build manifest (`setup/build_manifest.json`) listing the execution order

## Objective

Execute all build tasks in the correct dependency order. Each task's command describes what content to write to its output file. Dependencies must be executed before the tasks that depend on them.

## Setup

- `setup/build_tasks.json` — task definitions with dependencies
- `setup/outputs/` — directory where output files should be written

## Verification

```bash
python tests/verify.py
```

Checks that all output files exist with correct content and that the build manifest lists a valid execution order.
