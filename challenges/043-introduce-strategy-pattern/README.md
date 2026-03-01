# Challenge 043: Introduce Strategy Pattern

## Difficulty: Medium

## Task

The file `setup/payments.py` contains a single massive `process_payment(method, amount, details)` function with a long `if/elif` chain that handles different payment methods: credit card, PayPal, bank transfer, crypto, and gift card.

**Your job:** Refactor the monolithic function into the Strategy pattern with distinct strategy classes and a processor that dispatches to them.

## Requirements

After refactoring, `setup/payments.py` must have:

1. **Strategy classes** — one per payment type:
   - `CreditCardStrategy` with a `process(amount, details)` method
   - `PaypalStrategy` with a `process(amount, details)` method
   - `BankTransferStrategy` with a `process(amount, details)` method
   - `CryptoStrategy` with a `process(amount, details)` method
   - `GiftCardStrategy` with a `process(amount, details)` method

2. **`PaymentProcessor`** class with:
   - `register_strategy(method_name, strategy_instance)` — registers a strategy for a given method name
   - `process(method, amount, details)` — delegates to the registered strategy

3. The original `process_payment(method, amount, details)` function must still exist and produce the same results (it can internally use the strategy classes).

## Rules

- Only modify files in the `setup/` directory
- Each strategy class must encapsulate the full logic for its payment type
- All payment types must produce identical results to the original implementation
