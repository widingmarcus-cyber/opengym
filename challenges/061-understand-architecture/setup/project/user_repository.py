"""User repository for data access."""

from user_model import User


class UserRepository:
    def __init__(self):
        self._users = {}

    def save(self, user):
        self._users[user.user_id] = user
        return user

    def find_by_id(self, user_id):
        return self._users.get(user_id)

    def find_by_email(self, email):
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def find_all(self):
        return list(self._users.values())

    def delete(self, user_id):
        return self._users.pop(user_id, None)
