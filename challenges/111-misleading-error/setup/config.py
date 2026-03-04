class Discount:
    def __init__(self, code, percent):
        self.code = code
        self.percent = percent

DISCOUNTS = {
    "SAVE10": Discount("SAVE10", 10),
    "SAVE20": Discount("SAVE20", 20),
    "HALF": Discount("HALF", 50),
}

def get_discount(code):
    return DISCOUNTS.get(code)
