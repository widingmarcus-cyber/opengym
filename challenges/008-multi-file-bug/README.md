# Challenge 008: Multi-File Bug Hunt

## Difficulty: Hard

## Task

The project in `setup/` is a small order processing system. It has a bug: when a customer places an order with a discount code, the final price is calculated incorrectly.

The bug spans multiple files. You need to trace the flow from order creation through discount application to final price calculation to find and fix all the issues.

## Project Structure

```
setup/
├── app/
│   ├── __init__.py
│   ├── models.py      # Data classes for Order, Product, Discount
│   ├── discounts.py   # Discount lookup and validation
│   ├── pricing.py     # Price calculation logic
│   └── orders.py      # Order processing (entry point)
```

## How It Should Work

1. Customer creates an order with products and an optional discount code
2. System looks up the discount code and validates it
3. System calculates subtotal (sum of product prices * quantities)
4. System applies the discount to the subtotal
5. System returns the final order with correct total

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- The fix requires changes in multiple files
- All discount types must work: "percent" (e.g., 20% off) and "fixed" (e.g., $10 off)
