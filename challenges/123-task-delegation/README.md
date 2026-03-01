# Challenge 123: Task Delegation

## Difficulty: Hard
## Category: Task Splitting
## Dimension: Multi-Agent

## Description

A "Manager" agent breaks down a project into subtasks, and a "Worker" agent executes them. This tests whether agents can decompose problems effectively and whether another agent can follow task descriptions written by a different agent.

## Objective

Build a contact book module (`setup/contact_book.py`) with functions to add, remove, search, and list contacts. Each contact has name, phone, and email fields.

- **Manager Agent:** Breaks the project into subtask files in `setup/tasks/`
- **Worker Agent:** Reads the subtask files and implements each one

## Setup

- `setup/tasks/` — directory where the Manager writes subtask files
- `setup/contact_book.py` — created by the Manager with skeleton, implemented by the Worker

## Steps

1. **Step 1 (Manager):** Break down the project into subtasks and create the skeleton.
2. **Step 2 (Worker):** Read tasks and implement each function.

## Verification

```bash
python tests/verify.py
```

Tests that the contact book works correctly and that task files were created.
