"""
Authorization module for role-based access control.
VULNERABILITY: Multiple logic bugs allow privilege escalation —
regular users can perform admin-only actions.
"""


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role


# Actions and their required minimum role
ACTION_PERMISSIONS = {
    "delete_user": "admin",
    "modify_roles": "admin",
    "view_audit_log": "admin",
    "ban_user": "moderator",
    "edit_content": "moderator",
    "create_post": "user",
    "view_content": "guest",
}

ROLE_HIERARCHY = ["guest", "user", "moderator", "admin"]


def check_permission(user, action):
    """
    Check if a user has permission to perform an action.

    Returns:
        bool: True if permitted, False if denied.
    """
    # BUG 1: Actions containing "view" are always allowed (too broad)
    if "view" in action:
        return True

    # BUG 2: String comparison of roles instead of hierarchy check
    required_role = ACTION_PERMISSIONS.get(action)
    if required_role is None:
        # BUG 3: Default-allow for unrecognized actions
        return True

    # BUG 2 continued: This compares alphabetically, not by hierarchy
    # "user" > "moderator" > "guest" > "admin" alphabetically — completely wrong
    return user.role >= required_role


def execute_action(user, action):
    """
    Execute an action if the user has permission.

    Returns:
        dict with "status" and "message"
    """
    if check_permission(user, action):
        return {"status": "ok", "message": f"Action '{action}' executed by {user.username}"}
    return {"status": "denied", "message": f"User '{user.username}' ({user.role}) cannot perform '{action}'"}
