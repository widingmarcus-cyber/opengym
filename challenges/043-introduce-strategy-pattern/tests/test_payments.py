"""Tests for Challenge 043: Introduce Strategy Pattern."""

import sys
import inspect
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from payments import process_payment
import payments


# --- Tests that strategy classes exist ---

def test_credit_card_strategy_exists():
    assert hasattr(payments, "CreditCardStrategy"), "CreditCardStrategy class must exist"
    assert hasattr(payments.CreditCardStrategy, "process"), "CreditCardStrategy must have a process method"


def test_paypal_strategy_exists():
    assert hasattr(payments, "PaypalStrategy"), "PaypalStrategy class must exist"
    assert hasattr(payments.PaypalStrategy, "process"), "PaypalStrategy must have a process method"


def test_bank_transfer_strategy_exists():
    assert hasattr(payments, "BankTransferStrategy"), "BankTransferStrategy class must exist"
    assert hasattr(payments.BankTransferStrategy, "process"), "BankTransferStrategy must have a process method"


def test_crypto_strategy_exists():
    assert hasattr(payments, "CryptoStrategy"), "CryptoStrategy class must exist"
    assert hasattr(payments.CryptoStrategy, "process"), "CryptoStrategy must have a process method"


def test_gift_card_strategy_exists():
    assert hasattr(payments, "GiftCardStrategy"), "GiftCardStrategy class must exist"
    assert hasattr(payments.GiftCardStrategy, "process"), "GiftCardStrategy must have a process method"


# --- Test PaymentProcessor registry ---

def test_payment_processor_exists():
    assert hasattr(payments, "PaymentProcessor"), "PaymentProcessor class must exist"
    processor = payments.PaymentProcessor()
    assert hasattr(processor, "register_strategy"), "PaymentProcessor must have register_strategy method"
    assert hasattr(processor, "process"), "PaymentProcessor must have process method"


def test_payment_processor_register_and_process():
    processor = payments.PaymentProcessor()
    processor.register_strategy("credit_card", payments.CreditCardStrategy())
    result = processor.process("credit_card", 100.00, {
        "card_number": "4111-1111-1111-1111",
        "expiry": "12/26",
        "cvv": "123",
    })
    assert result["success"] is True
    assert result["method"] == "credit_card"


# --- Tests that original function still works correctly ---

def test_credit_card_payment():
    result = process_payment("credit_card", 100.00, {
        "card_number": "4111111111111111",
        "expiry": "12/26",
        "cvv": "123",
    })
    assert result["success"] is True
    assert result["fee"] == round(100.00 * 0.029 + 0.30, 2)
    assert result["total"] == round(100.00 + result["fee"], 2)
    assert result["masked_card"] == "****-****-****-1111"


def test_paypal_payment():
    result = process_payment("paypal", 50.00, {"email": "User@Example.COM"})
    assert result["success"] is True
    assert result["paypal_email"] == "user@example.com"
    assert result["fee"] == round(50.00 * 0.034 + 0.49, 2)


def test_bank_transfer_payment():
    result = process_payment("bank_transfer", 200.00, {
        "routing_number": "123456789",
        "account_number": "9876543210",
    })
    assert result["success"] is True
    assert result["fee"] == 1.50
    assert result["masked_account"] == "****3210"
