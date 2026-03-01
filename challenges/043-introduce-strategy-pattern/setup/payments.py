"""Payment processing module with multiple payment method support."""

import hashlib
import math


def process_payment(method, amount, details):
    """Process a payment using the given method."""
    if amount <= 0:
        return {"success": False, "error": "amount must be positive"}

    if method == "credit_card":
        card_number = details.get("card_number", "")
        expiry = details.get("expiry", "")
        cvv = details.get("cvv", "")

        if not card_number or not expiry or not cvv:
            return {"success": False, "error": "missing credit card details"}

        if len(card_number.replace("-", "").replace(" ", "")) != 16:
            return {"success": False, "error": "invalid card number"}

        fee = round(amount * 0.029 + 0.30, 2)
        total = round(amount + fee, 2)
        masked = "****-****-****-" + card_number.replace("-", "").replace(" ", "")[-4:]

        return {
            "success": True,
            "method": "credit_card",
            "amount": amount,
            "fee": fee,
            "total": total,
            "masked_card": masked,
            "reference": hashlib.sha256(f"cc:{amount}:{card_number[-4:]}".encode()).hexdigest()[:12],
        }

    elif method == "paypal":
        email = details.get("email", "")

        if not email or "@" not in email:
            return {"success": False, "error": "invalid paypal email"}

        fee = round(amount * 0.034 + 0.49, 2)
        total = round(amount + fee, 2)

        return {
            "success": True,
            "method": "paypal",
            "amount": amount,
            "fee": fee,
            "total": total,
            "paypal_email": email.lower(),
            "reference": hashlib.sha256(f"pp:{amount}:{email}".encode()).hexdigest()[:12],
        }

    elif method == "bank_transfer":
        routing = details.get("routing_number", "")
        account = details.get("account_number", "")

        if not routing or not account:
            return {"success": False, "error": "missing bank details"}

        if len(routing) != 9:
            return {"success": False, "error": "routing number must be 9 digits"}

        fee = 1.50
        total = round(amount + fee, 2)
        masked_account = "****" + account[-4:]

        return {
            "success": True,
            "method": "bank_transfer",
            "amount": amount,
            "fee": fee,
            "total": total,
            "masked_account": masked_account,
            "reference": hashlib.sha256(f"bt:{amount}:{account[-4:]}".encode()).hexdigest()[:12],
        }

    elif method == "crypto":
        wallet = details.get("wallet_address", "")
        currency = details.get("currency", "BTC")

        if not wallet or len(wallet) < 20:
            return {"success": False, "error": "invalid wallet address"}

        rates = {"BTC": 45000, "ETH": 3000, "LTC": 150}
        rate = rates.get(currency.upper(), None)
        if rate is None:
            return {"success": False, "error": f"unsupported currency: {currency}"}

        crypto_amount = round(amount / rate, 8)
        fee = round(amount * 0.015, 2)
        total = round(amount + fee, 2)

        return {
            "success": True,
            "method": "crypto",
            "amount": amount,
            "fee": fee,
            "total": total,
            "crypto_amount": crypto_amount,
            "currency": currency.upper(),
            "wallet": wallet,
            "reference": hashlib.sha256(f"cr:{amount}:{wallet[:8]}".encode()).hexdigest()[:12],
        }

    elif method == "gift_card":
        card_code = details.get("card_code", "")
        pin = details.get("pin", "")

        if not card_code or not pin:
            return {"success": False, "error": "missing gift card details"}

        if len(card_code) != 16:
            return {"success": False, "error": "gift card code must be 16 characters"}

        balance = details.get("balance", 0)
        if amount > balance:
            return {"success": False, "error": "insufficient gift card balance"}

        remaining = round(balance - amount, 2)
        fee = 0.0
        total = amount

        return {
            "success": True,
            "method": "gift_card",
            "amount": amount,
            "fee": fee,
            "total": total,
            "remaining_balance": remaining,
            "reference": hashlib.sha256(f"gc:{amount}:{card_code[:4]}".encode()).hexdigest()[:12],
        }

    else:
        return {"success": False, "error": f"unknown payment method: {method}"}
