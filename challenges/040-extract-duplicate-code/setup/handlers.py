"""Record handlers for different entity types."""


def handle_user(data):
    """Process a user record."""
    if not isinstance(data, dict):
        return {"valid": False, "record": None, "summary": "invalid input"}

    required = ["name", "age", "email"]
    for field in required:
        if field not in data:
            return {"valid": False, "record": None, "summary": f"missing field: {field}"}

    try:
        name = str(data["name"]).strip()
        age = int(data["age"])
        email = str(data["email"]).strip().lower()
    except (ValueError, TypeError):
        return {"valid": False, "record": None, "summary": "type conversion failed"}

    if not name or age < 0 or not email:
        return {"valid": False, "record": None, "summary": "validation failed"}

    record = {"name": name, "age": age, "email": email}
    summary = " | ".join(f"{k}={v}" for k, v in record.items())
    return {"valid": True, "record": record, "summary": summary}


def handle_product(data):
    """Process a product record."""
    if not isinstance(data, dict):
        return {"valid": False, "record": None, "summary": "invalid input"}

    required = ["title", "price", "quantity"]
    for field in required:
        if field not in data:
            return {"valid": False, "record": None, "summary": f"missing field: {field}"}

    try:
        title = str(data["title"]).strip()
        price = float(data["price"])
        quantity = int(data["quantity"])
    except (ValueError, TypeError):
        return {"valid": False, "record": None, "summary": "type conversion failed"}

    if not title or price < 0 or quantity < 0:
        return {"valid": False, "record": None, "summary": "validation failed"}

    record = {"title": title, "price": price, "quantity": quantity}
    summary = " | ".join(f"{k}={v}" for k, v in record.items())
    return {"valid": True, "record": record, "summary": summary}


def handle_order(data):
    """Process an order record."""
    if not isinstance(data, dict):
        return {"valid": False, "record": None, "summary": "invalid input"}

    required = ["order_id", "amount", "status"]
    for field in required:
        if field not in data:
            return {"valid": False, "record": None, "summary": f"missing field: {field}"}

    try:
        order_id = str(data["order_id"]).strip()
        amount = float(data["amount"])
        status = str(data["status"]).strip().lower()
    except (ValueError, TypeError):
        return {"valid": False, "record": None, "summary": "type conversion failed"}

    if not order_id or amount < 0 or not status:
        return {"valid": False, "record": None, "summary": "validation failed"}

    record = {"order_id": order_id, "amount": amount, "status": status}
    summary = " | ".join(f"{k}={v}" for k, v in record.items())
    return {"valid": True, "record": record, "summary": summary}


def handle_payment(data):
    """Process a payment record."""
    if not isinstance(data, dict):
        return {"valid": False, "record": None, "summary": "invalid input"}

    required = ["payment_id", "total", "method"]
    for field in required:
        if field not in data:
            return {"valid": False, "record": None, "summary": f"missing field: {field}"}

    try:
        payment_id = str(data["payment_id"]).strip()
        total = float(data["total"])
        method = str(data["method"]).strip().lower()
    except (ValueError, TypeError):
        return {"valid": False, "record": None, "summary": "type conversion failed"}

    if not payment_id or total < 0 or not method:
        return {"valid": False, "record": None, "summary": "validation failed"}

    record = {"payment_id": payment_id, "total": total, "method": method}
    summary = " | ".join(f"{k}={v}" for k, v in record.items())
    return {"valid": True, "record": record, "summary": summary}
