# Challenge 127: Plan Then Execute

## Difficulty: Hard
## Category: Plan-Execute
## Dimension: Planning

## Description

Write a detailed implementation plan first, then implement it. Both the plan and the code are verified. This tests whether an agent can separate planning from execution and whether it follows its own plan.

## Objective

1. **Step 1:** Write a detailed plan for an inventory management module to `setup/plan.md`. No code yet -- only the plan.
2. **Step 2:** Implement the inventory module in `setup/inventory.py` following the plan.

## Required Functions

- `add_item(name, quantity, price)`: Add item to inventory
- `remove_item(name, quantity)`: Remove quantity of item (error if insufficient)
- `get_item(name)`: Return item details or None
- `total_value()`: Return total value of all inventory
- `low_stock(threshold)`: Return list of items with quantity below threshold

## Setup

- `setup/plan.md` — empty file for the plan
- `setup/inventory.py` — empty file for the implementation

## Steps

1. **Step 1:** Write the plan (no code).
2. **Step 2:** Implement following the plan.

## Verification

```bash
python tests/verify.py
```

Tests that the plan exists and is substantive, and that all inventory functions work correctly.
