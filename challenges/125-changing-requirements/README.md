# Challenge 125: Changing Requirements

## Difficulty: Medium
## Category: Requirement Adaptation
## Dimension: Planning

## Description

Build a feature, then adapt when requirements change. This tests whether an agent can extend existing code rather than starting from scratch when new requirements arrive.

## Objective

1. **Step 1:** Implement a basic temperature converter with Celsius-to-Fahrenheit and Fahrenheit-to-Celsius functions.
2. **Step 2:** Requirements change! Add Kelvin support and a unified `convert()` function that handles all 6 conversion directions, while keeping the original functions working.

## Setup

- `setup/converter.py` — empty file to implement

## Steps

1. **Step 1:** Implement basic C/F converter.
2. **Step 2:** Extend with Kelvin and unified convert function.

## Verification

```bash
python tests/verify.py
```

Tests all conversion functions and the unified convert() interface.
