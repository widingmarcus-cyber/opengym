"""
CLI tool module with database query and network ping functions.
VULNERABILITY: Both functions have injection vulnerabilities —
SQL injection in query_user and command injection in ping_host.
"""

import os
import sqlite3
import re


def query_user(db_path, username):
    """
    Query the SQLite database for a user by username.

    Returns:
        dict with "status" and either "user" or "message"
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # BUG: SQL injection — string formatting instead of parameterized query
        query = f"SELECT username, email, role FROM users WHERE username = '{username}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            users = [{"username": r[0], "email": r[1], "role": r[2]} for r in rows]
            return {"status": "ok", "users": users}
        return {"status": "ok", "users": []}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def ping_host(hostname):
    """
    Ping a host and return the result.

    Returns:
        dict with "status" and "message"
    """
    # BUG: Command injection — unsanitized input passed to shell
    ret = os.system(f"ping -c 1 {hostname} > /dev/null 2>&1")
    if ret == 0:
        return {"status": "ok", "message": f"Host {hostname} is reachable"}
    return {"status": "error", "message": f"Host {hostname} is not reachable"}
