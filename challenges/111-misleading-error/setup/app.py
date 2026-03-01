from config import get_discount
from utils import calculate_total, apply_discount, Item

def process_order(items, discount_code=None):
    total = calculate_total(items)
    if discount_code:
        discount = get_discount(discount_code)
        total = apply_discount(total, discount)
    return round(total, 2)
