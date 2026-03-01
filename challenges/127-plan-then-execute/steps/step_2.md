Now implement the inventory module in setup/inventory.py following the plan you wrote in setup/plan.md. The module must support:
- add_item(name, quantity, price): Add item to inventory
- remove_item(name, quantity): Remove quantity of item (error if insufficient)
- get_item(name): Return item details or None
- total_value(): Return total value of all inventory
- low_stock(threshold): Return list of items with quantity below threshold
