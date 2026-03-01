# Challenge 111: Misleading Error

The application in `setup/` crashes with this error:

```
Traceback (most recent call last):
  File "app.py", line 28, in process_order
    total = calculate_total(items)
  File "utils.py", line 42, in calculate_total
    return sum(item.price * item.quantity for item in items)
AttributeError: 'NoneType' object has no attribute 'price'
```

Find and fix the bug so all tests pass. The error occurs when processing an order with a discount code.
