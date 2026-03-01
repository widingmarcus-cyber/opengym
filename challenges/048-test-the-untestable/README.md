# Challenge 048: Test the Untestable

## Difficulty: Medium

## Task

The file `setup/notifier.py` contains a notification module with hard-coded dependencies on a database, email service, and file logger. These dependencies cannot be used directly in tests.

**Your job:** Write tests in `setup/test_notifier.py` that use `unittest.mock.patch` to mock the internal dependencies and thoroughly test the `send_notification` function's logic.

## Module Under Test

`send_notification(user_id, message)` does the following:
1. Calls `_get_user_from_db(user_id)` to look up a user record (returns a dict with "name" and "email")
2. Calls `_send_email(email, formatted_message)` to send the notification
3. Calls `_log_to_file(log_entry)` to log the notification
4. Returns a dict with "success", "user", and "message_sent" keys

If the user is not found, it returns `{"success": False, "error": "User not found"}`.
If the email fails, it returns `{"success": False, "error": "Email delivery failed"}`.

## Rules

- Only modify files in the `setup/` directory
- Write your tests in `setup/test_notifier.py`
- You must use `unittest.mock.patch` to mock `_get_user_from_db`, `_send_email`, and `_log_to_file`
- Tests must not require a real database, email service, or filesystem

## Examples

```python
# With mocking:
with patch('notifier._get_user_from_db') as mock_db:
    mock_db.return_value = {"name": "Alice", "email": "alice@test.com"}
    # ... test send_notification
```
