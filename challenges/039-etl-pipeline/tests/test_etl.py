"""Tests for Challenge 039: ETL Pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from etl import extract_customers, extract_orders, extract_products, transform, generate_report

SETUP_DIR = Path(__file__).parent.parent / "setup"
CSV_PATH = str(SETUP_DIR / "customers.csv")
JSON_PATH = str(SETUP_DIR / "orders.json")
XML_PATH = str(SETUP_DIR / "products.xml")


def test_extract_customers():
    customers = extract_customers(CSV_PATH)
    assert isinstance(customers, list)
    assert len(customers) == 5
    assert customers[0]["id"] == "C001"
    assert customers[0]["name"] == "Alice Johnson"
    assert customers[0]["email"] == "alice@example.com"


def test_extract_orders():
    orders = extract_orders(JSON_PATH)
    assert isinstance(orders, list)
    assert len(orders) == 10
    assert orders[0]["id"] == "O001"
    assert orders[0]["customer_id"] == "C001"
    assert orders[0]["quantity"] == 2


def test_extract_products():
    products = extract_products(XML_PATH)
    assert isinstance(products, list)
    assert len(products) == 5
    names = {p["name"] for p in products}
    assert names == {"Laptop", "Headphones", "Keyboard", "Mouse", "Monitor"}
    laptop = [p for p in products if p["name"] == "Laptop"][0]
    assert abs(float(laptop["price"]) - 999.99) < 0.01


def test_transform_count():
    customers = extract_customers(CSV_PATH)
    orders = extract_orders(JSON_PATH)
    products = extract_products(XML_PATH)
    result = transform(customers, orders, products)
    assert isinstance(result, list)
    assert len(result) == 10


def test_transform_fields():
    customers = extract_customers(CSV_PATH)
    orders = extract_orders(JSON_PATH)
    products = extract_products(XML_PATH)
    result = transform(customers, orders, products)
    first = [r for r in result if r["order_id"] == "O001"][0]
    assert first["customer_name"] == "Alice Johnson"
    assert first["product_name"] == "Laptop"
    assert first["quantity"] == 2
    assert abs(first["unit_price"] - 999.99) < 0.01
    assert abs(first["total_price"] - 1999.98) < 0.01


def test_transform_total_price():
    customers = extract_customers(CSV_PATH)
    orders = extract_orders(JSON_PATH)
    products = extract_products(XML_PATH)
    result = transform(customers, orders, products)
    o005 = [r for r in result if r["order_id"] == "O005"][0]
    assert abs(o005["total_price"] - 149.95) < 0.01


def test_report_total_revenue():
    customers = extract_customers(CSV_PATH)
    orders = extract_orders(JSON_PATH)
    products = extract_products(XML_PATH)
    transformed = transform(customers, orders, products)
    report = generate_report(transformed)
    assert abs(report["total_revenue"] - 7259.76) < 0.01


def test_report_top_customer():
    customers = extract_customers(CSV_PATH)
    orders = extract_orders(JSON_PATH)
    products = extract_products(XML_PATH)
    transformed = transform(customers, orders, products)
    report = generate_report(transformed)
    assert report["top_customer"] == "Diana Prince"
    assert isinstance(report["orders_per_product"], dict)
    assert report["orders_per_product"]["Laptop"] == 3
    assert report["orders_per_product"]["Monitor"] == 1
