"""Product repository for data access."""

from product_model import Product


class ProductRepository:
    def __init__(self):
        self._products = {}

    def save(self, product):
        self._products[product.product_id] = product
        return product

    def find_by_id(self, product_id):
        return self._products.get(product_id)

    def find_all(self):
        return list(self._products.values())

    def find_by_category(self, category):
        return [p for p in self._products.values() if p.category == category]

    def delete(self, product_id):
        return self._products.pop(product_id, None)

    def update_stock(self, product_id, new_stock):
        product = self.find_by_id(product_id)
        if product:
            product.stock = new_stock
            return product
        return None
