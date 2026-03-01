"""User data model."""

from datetime import datetime


class User:
    def __init__(self, user_id, name, email, role="customer"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }

    def is_admin(self):
        return self.role == "admin"
