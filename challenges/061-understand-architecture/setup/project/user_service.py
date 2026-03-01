"""User business logic service."""

from user_repository import UserRepository
from user_model import User
from order_service import OrderService


class UserService:
    def __init__(self, repository=None):
        self.repository = repository or UserRepository()

    def create_user(self, name, email, role="customer"):
        if self.repository.find_by_email(email):
            raise ValueError("Email already registered")
        user_id = len(self.repository.find_all()) + 1
        user = User(user_id, name, email, role)
        return self.repository.save(user)

    def get_user(self, user_id):
        return self.repository.find_by_id(user_id)

    def get_user_by_email(self, email):
        return self.repository.find_by_email(email)

    def authenticate(self, email):
        user = self.repository.find_by_email(email)
        if not user:
            raise ValueError("Authentication failed")
        return user

    def get_user_order_history(self, user_id):
        order_service = OrderService()
        return order_service.get_user_orders(user_id)

    def list_users(self):
        return self.repository.find_all()
