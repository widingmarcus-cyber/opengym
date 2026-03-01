USERS_DB = {
    "L-42": {"name": "Alice", "email": "alice@legacy.com", "migrated": True},
    43: {"name": "Bob", "email": "bob@example.com", "migrated": False},
    44: {"name": "Carol", "email": "carol@example.com", "migrated": False},
}

class UserRepository:
    def find_by_id(self, user_id):
        """Find user by ID. Supports both integer and legacy string IDs."""
        return USERS_DB.get(user_id)
