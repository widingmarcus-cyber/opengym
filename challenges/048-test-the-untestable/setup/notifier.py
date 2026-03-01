"""Notification module with hard-coded dependencies."""


def _get_user_from_db(user_id):
    """Look up a user in the database. Requires a live database connection."""
    raise RuntimeError("Cannot connect to database in test environment")


def _send_email(email, message):
    """Send an email. Requires a live email service."""
    raise RuntimeError("Cannot connect to email service in test environment")


def _log_to_file(message):
    """Log a message to a file. Requires filesystem access."""
    raise RuntimeError("Cannot write to log file in test environment")


def send_notification(user_id, message):
    """Send a notification to a user.

    Looks up the user, sends them an email, and logs the action.
    Returns a result dict indicating success or failure.
    """
    try:
        user = _get_user_from_db(user_id)
    except Exception:
        return {"success": False, "error": "User not found"}

    if user is None:
        return {"success": False, "error": "User not found"}

    formatted_message = f"Hello {user['name']}, {message}"

    try:
        _send_email(user["email"], formatted_message)
    except Exception:
        return {"success": False, "error": "Email delivery failed"}

    log_entry = f"Notification sent to {user['email']}: {formatted_message}"
    try:
        _log_to_file(log_entry)
    except Exception:
        pass

    return {
        "success": True,
        "user": user["name"],
        "message_sent": formatted_message,
    }
