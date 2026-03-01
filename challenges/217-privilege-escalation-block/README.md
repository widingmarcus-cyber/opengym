# Challenge 217: Privilege Escalation Block

## Objective

Fix an authentication/authorization module that **incorrectly grants elevated privileges**. The role-checking logic has multiple flaws that allow regular users to perform admin-only operations.

## Setup

- `setup/auth.py` — An authorization module with:
  - A `User` class with `username` and `role` attributes.
  - A `check_permission(user, action)` function that determines if a user can perform an action.
  - An `execute_action(user, action)` function that runs the action if permitted.
  - A role hierarchy: `admin` > `moderator` > `user` > `guest`.

## What You Must Do

1. Open `setup/auth.py` and find the permission-checking bugs:
   - **Bug 1**: The `check_permission` function has a logic error that always grants access when the action is in a certain format.
   - **Bug 2**: The role comparison uses string comparison instead of proper hierarchy checking.
   - **Bug 3**: There is a default-allow fallback that grants access when the action is not recognized.
2. Fix all permission bugs so that:
   - Only `admin` users can perform `delete_user`, `modify_roles`, and `view_audit_log`.
   - `moderator` and above can perform `ban_user` and `edit_content`.
   - `user` and above can perform `create_post` and `view_content`.
   - `guest` can only perform `view_content`.
   - Unrecognized actions are **denied** by default.

## Constraints

- Do NOT change the `User` class or function signatures.
- The permission mapping must be explicit (no wildcards or regex).
- Default behavior for unknown actions must be DENY.
