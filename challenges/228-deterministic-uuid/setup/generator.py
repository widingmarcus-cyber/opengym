"""UUID generator for user records."""

import uuid


def generate_id(name: str) -> str:
    """Generate a unique ID for a user.

    Args:
        name: The user's name.

    Returns:
        A UUID string.
    """
    # BUG: This uses random UUIDs — not deterministic!
    return str(uuid.uuid4())


def generate_batch(names: list) -> dict:
    """Generate unique IDs for a batch of users.

    Args:
        names: List of user names.

    Returns:
        Dictionary mapping name -> UUID string.
    """
    result = {}
    for name in names:
        result[name] = str(uuid.uuid4())
    return result


if __name__ == "__main__":
    # Demo
    print("Single:", generate_id("alice"))
    print("Single:", generate_id("alice"))  # Should be same as above if deterministic
    print("Batch:", generate_batch(["alice", "bob", "charlie"]))
