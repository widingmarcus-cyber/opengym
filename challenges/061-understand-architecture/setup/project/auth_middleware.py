"""Authentication middleware."""

from user_service import UserService


class AuthMiddleware:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def authenticate(self, request):
        token = request.get("authorization")
        if not token:
            return None, {"status": "error", "message": "No authorization token"}

        email = self._decode_token(token)
        if not email:
            return None, {"status": "error", "message": "Invalid token"}

        try:
            user = self.user_service.authenticate(email)
            return user, None
        except ValueError:
            return None, {"status": "error", "message": "Authentication failed"}

    def require_admin(self, request):
        user, error = self.authenticate(request)
        if error:
            return None, error
        if not user.is_admin():
            return None, {"status": "error", "message": "Admin access required"}
        return user, None

    def _decode_token(self, token):
        if token.startswith("Bearer "):
            return token[7:]
        return None
