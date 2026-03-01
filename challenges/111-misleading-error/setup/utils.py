class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

def calculate_total(items):
    """Calculate total price for a list of items."""
    return sum(item.price * item.quantity for item in items)

def apply_discount(total, discount):
    """Apply a discount to a total. Discount must not be None."""
    if discount is None:
        raise ValueError("Discount cannot be None")
    reduction = total * (discount.percent / 100)
    return total - reduction
