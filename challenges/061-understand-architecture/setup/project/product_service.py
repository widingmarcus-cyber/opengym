"""Product business logic service."""

from product_repository import ProductRepository
from product_model import Product


class ProductService:
    def __init__(self, repository=None):
        self.repository = repository or ProductRepository()

    def create_product(self, name, price, stock, category):
        product_id = len(self.repository.find_all()) + 1
        product = Product(product_id, name, price, stock, category)
        return self.repository.save(product)

    def get_product(self, product_id):
        product = self.repository.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        return product

    def list_products(self, category=None):
        if category:
            return self.repository.find_by_category(category)
        return self.repository.find_all()

    def check_availability(self, product_id, quantity):
        product = self.get_product(product_id)
        return product.stock >= quantity

    def reduce_stock(self, product_id, quantity):
        product = self.get_product(product_id)
        if product.stock < quantity:
            raise ValueError("Insufficient stock")
        self.repository.update_stock(product_id, product.stock - quantity)
