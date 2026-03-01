import json
import os
import sys
import sqlite3
import tempfile
import re

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from tool import query_user, ping_host


def _create_test_db():
    """Create a temporary SQLite database with test users."""
    db_path = os.path.join(tempfile.gettempdir(), "test_users_216.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, email TEXT, role TEXT)")
    cursor.execute("INSERT INTO users VALUES ('alice', 'alice@example.com', 'admin')")
    cursor.execute("INSERT INTO users VALUES ('bob', 'bob@example.com', 'user')")
    cursor.execute("INSERT INTO users VALUES ('charlie', 'charlie@example.com', 'user')")
    conn.commit()
    conn.close()
    return db_path


def test_legitimate_query():
    """Legitimate query for a known user should return that user."""
    db_path = _create_test_db()
    result = query_user(db_path, "alice")
    if result.get("status") != "ok":
        print(json.dumps({"test": "legitimate_query", "passed": False,
                          "message": f"Expected status ok, got: {result}"}))
        return
    users = result.get("users", [])
    if len(users) != 1 or users[0].get("username") != "alice":
        print(json.dumps({"test": "legitimate_query", "passed": False,
                          "message": f"Expected alice, got: {users}"}))
        return
    print(json.dumps({"test": "legitimate_query", "passed": True, "message": "OK"}))


def test_sql_injection_blocked():
    """SQL injection attempt must NOT return all users."""
    db_path = _create_test_db()
    result = query_user(db_path, "' OR 1=1 --")
    users = result.get("users", [])
    if len(users) > 1:
        print(json.dumps({"test": "sql_injection_blocked", "passed": False,
                          "message": f"SQL injection succeeded — returned {len(users)} users instead of 0"}))
        return
    # Also test UNION injection
    result2 = query_user(db_path, "' UNION SELECT username, email, role FROM users --")
    users2 = result2.get("users", [])
    if len(users2) > 1:
        print(json.dumps({"test": "sql_injection_blocked", "passed": False,
                          "message": f"UNION injection succeeded — returned {len(users2)} users"}))
        return
    print(json.dumps({"test": "sql_injection_blocked", "passed": True, "message": "OK"}))


def test_parameterized_query_used():
    """The source code must use parameterized queries (? placeholders), not string formatting."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "tool.py")
    with open(source_path, "r") as f:
        source = f.read()
    # Check that f-string or format-based SQL is gone and ? placeholder is used
    if "f\"SELECT" in source or "f'SELECT" in source or ".format(" in source or "% " in source:
        print(json.dumps({"test": "parameterized_query_used", "passed": False,
                          "message": "query_user still uses string formatting for SQL query"}))
        return
    if "?" not in source:
        print(json.dumps({"test": "parameterized_query_used", "passed": False,
                          "message": "query_user does not use ? parameterized placeholders"}))
        return
    print(json.dumps({"test": "parameterized_query_used", "passed": True, "message": "OK"}))


def test_no_os_system():
    """ping_host must not use os.system() — must use subprocess instead."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "tool.py")
    with open(source_path, "r") as f:
        source = f.read()
    if "os.system(" in source:
        print(json.dumps({"test": "no_os_system", "passed": False,
                          "message": "ping_host still uses os.system()"}))
        return
    if "shell=True" in source:
        print(json.dumps({"test": "no_os_system", "passed": False,
                          "message": "ping_host uses shell=True which is still vulnerable"}))
        return
    if "subprocess" not in source:
        print(json.dumps({"test": "no_os_system", "passed": False,
                          "message": "ping_host does not use subprocess module"}))
        return
    print(json.dumps({"test": "no_os_system", "passed": True, "message": "OK"}))


def test_command_injection_blocked():
    """Command injection via hostname must be blocked."""
    # These malicious hostnames should be rejected or at minimum not execute injected commands
    malicious_hosts = [
        "localhost; echo PWNED",
        "localhost && echo PWNED",
        "localhost | echo PWNED",
        "$(echo PWNED)",
    ]
    for host in malicious_hosts:
        result = ping_host(host)
        if result.get("status") == "ok":
            print(json.dumps({"test": "command_injection_blocked", "passed": False,
                              "message": f"Malicious hostname '{host}' was not rejected"}))
            return
    print(json.dumps({"test": "command_injection_blocked", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_legitimate_query()
    test_sql_injection_blocked()
    test_parameterized_query_used()
    test_no_os_system()
    test_command_injection_blocked()
