# Challenge 098: Full-Stack Bug Fix

## Difficulty: Hard

## Description

A user registration and order management system has been deployed, but users are
reporting multiple issues across the application. The bugs span several layers of
the codebase -- models, validators, serializers, and the API glue that ties them
together.

### Reported Issues

1. **Email validation is too permissive.** Users are able to register with email
   addresses like `user@` or `user@domain` (no TLD dot). The validator should
   reject any email that does not contain both an `@` symbol and a `.` in the
   domain portion.

2. **Orders with invalid quantities are accepted.** The system allows orders
   where the item quantity is zero or negative. Both cases should be rejected
   with a `ValueError`.

3. **The API returns incorrect pricing information.** Order totals and per-item
   line totals in API responses are wrong. The total price for an order should
   equal the sum of `quantity * price` for every item, and each serialized item
   should include a `line_total` that equals `quantity * price`.

## Your Task

Trace the bugs across all four source files in the `setup/` directory and apply
the minimal fixes needed so that every test in `tests/test_full_stack.py` passes.

```
setup/
  models.py       - User, OrderItem, and Order dataclasses
  validators.py   - Email and order validation functions
  serializers.py  - Functions that convert models to API-ready dicts
  api.py          - High-level registration and order creation functions
```

## Verification

```bash
pytest tests/ -v
```

All 10 tests must pass.
