"""Product API controller."""

from product_service import ProductService


class ProductController:
    def __init__(self, service=None):
        self.service = service or ProductService()

    def get_products(self, request):
        category = request.get("category")
        products = self.service.list_products(category)
        return {
            "status": "success",
            "data": [p.to_dict() for p in products],
        }

    def get_product(self, request):
        product_id = request["product_id"]
        try:
            product = self.service.get_product(product_id)
            return {"status": "success", "data": product.to_dict()}
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def create_product(self, request):
        product = self.service.create_product(
            name=request["name"],
            price=request["price"],
            stock=request["stock"],
            category=request["category"],
        )
        return {"status": "success", "data": product.to_dict()}
