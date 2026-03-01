from repos.user import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_profile(self, user_id):
        """Get user profile by ID."""
        # Tries integer lookup only
        user = self.repo.find_by_id(user_id)
        return user  # Returns None if not found, should also try legacy format
