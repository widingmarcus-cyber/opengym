import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from auth import User, check_permission, execute_action


def test_admin_can_do_admin_actions():
    """Admin users should be able to perform all admin actions."""
    admin = User("root", "admin")
    for action in ["delete_user", "modify_roles", "view_audit_log", "ban_user", "edit_content", "create_post", "view_content"]:
        if not check_permission(admin, action):
            print(json.dumps({"test": "admin_can_do_admin_actions", "passed": False,
                              "message": f"Admin was denied action '{action}'"}))
            return
    print(json.dumps({"test": "admin_can_do_admin_actions", "passed": True, "message": "OK"}))


def test_regular_user_cannot_delete():
    """Regular user must NOT be able to delete_user or modify_roles."""
    user = User("bob", "user")
    for action in ["delete_user", "modify_roles"]:
        if check_permission(user, action):
            print(json.dumps({"test": "regular_user_cannot_delete", "passed": False,
                              "message": f"Regular user was allowed '{action}' — privilege escalation!"}))
            return
    print(json.dumps({"test": "regular_user_cannot_delete", "passed": True, "message": "OK"}))


def test_guest_cannot_create_post():
    """Guest must NOT be able to create_post — only view_content."""
    guest = User("anon", "guest")
    if check_permission(guest, "create_post"):
        print(json.dumps({"test": "guest_cannot_create_post", "passed": False,
                          "message": "Guest was allowed to create_post — privilege escalation!"}))
        return
    if not check_permission(guest, "view_content"):
        print(json.dumps({"test": "guest_cannot_create_post", "passed": False,
                          "message": "Guest was denied view_content — should be allowed"}))
        return
    print(json.dumps({"test": "guest_cannot_create_post", "passed": True, "message": "OK"}))


def test_unknown_action_denied():
    """Unrecognized actions must be DENIED by default."""
    user = User("bob", "user")
    admin = User("root", "admin")
    for u in [user, admin]:
        if check_permission(u, "launch_missiles"):
            print(json.dumps({"test": "unknown_action_denied", "passed": False,
                              "message": f"Unknown action 'launch_missiles' was allowed for {u.role}"}))
            return
    print(json.dumps({"test": "unknown_action_denied", "passed": True, "message": "OK"}))


def test_view_audit_log_admin_only():
    """view_audit_log must require admin role, not be open to everyone."""
    user = User("bob", "user")
    guest = User("anon", "guest")
    moderator = User("mod", "moderator")
    for u in [user, guest, moderator]:
        if check_permission(u, "view_audit_log"):
            print(json.dumps({"test": "view_audit_log_admin_only", "passed": False,
                              "message": f"view_audit_log was allowed for {u.role} — should be admin only"}))
            return
    admin = User("root", "admin")
    if not check_permission(admin, "view_audit_log"):
        print(json.dumps({"test": "view_audit_log_admin_only", "passed": False,
                          "message": "view_audit_log was denied for admin"}))
        return
    print(json.dumps({"test": "view_audit_log_admin_only", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_admin_can_do_admin_actions()
    test_regular_user_cannot_delete()
    test_guest_cannot_create_post()
    test_unknown_action_denied()
    test_view_audit_log_admin_only()
