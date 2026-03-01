# Challenge 050: Build Test Fixture

## Difficulty: Hard

## Task

You are given a simple e-commerce data model with `User`, `Product`, and `Order` dataclasses, plus an `InMemoryDB` class for storage. Your job is to:

1. Create reusable test fixtures in `setup/fixtures.py` that set up a populated database with sample data
2. Write tests in `setup/test_orders.py` that use those fixtures to test order processing logic

## Files

- `setup/models.py` — Dataclasses for `User`, `Product`, and `Order`
- `setup/database.py` — `InMemoryDB` class with `insert`, `get`, `query`, and `delete` methods
- `setup/fixtures.py` — **Write your fixtures here** (stub file)
- `setup/test_orders.py` — **Write your tests here** (stub file)

## Requirements

### Fixtures (`fixtures.py`)

Create functions that return pre-populated test data:

- `create_sample_users()` — Returns a list of at least 3 User objects
- `create_sample_products()` — Returns a list of at least 3 Product objects
- `create_populated_db()` — Returns an InMemoryDB pre-loaded with sample users and products
- `create_sample_order(db)` — Creates and returns a valid Order using data from the given db

### Tests (`test_orders.py`)

Write at least 6 tests covering:

- Creating an order with valid user and products
- Order total calculation
- Querying orders from the database
- Order with empty product list
- Multiple orders for the same user
- Fixture data integrity (users and products exist in the db)

## Rules

- Only modify files in the `setup/` directory
- You must use the fixtures from `fixtures.py` in your tests
- Tests must be self-contained (each test sets up its own db via fixtures)

## Data Model

```python
@dataclass
class User:
    id: str
    name: str
    email: str

@dataclass
class Product:
    id: str
    name: str
    price: float

@dataclass
class Order:
    id: str
    user_id: str
    product_ids: list
    total: float
```
