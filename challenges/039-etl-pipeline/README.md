# Challenge 039: ETL Pipeline

## Difficulty: Hard

## Task

Build an Extract-Transform-Load pipeline that reads data from three different file formats, joins them together, and generates a summary report. Implement the pipeline in `setup/etl.py`.

## Requirements

Implement these functions in `setup/etl.py`:

### Extract

1. `extract_customers(csv_path)` -- Read a CSV file and return a list of customer dictionaries with keys: `id`, `name`, `email`.
2. `extract_orders(json_path)` -- Read a JSON file and return a list of order dictionaries with keys: `id`, `customer_id`, `product_id`, `quantity`, `date`.
3. `extract_products(xml_path)` -- Read an XML file and return a list of product dictionaries with keys: `id`, `name`, `price`.

### Transform

4. `transform(customers, orders, products)` -- Join the three datasets together. Return a list of dictionaries, one per order, each containing: `order_id`, `customer_name`, `product_name`, `quantity`, `unit_price`, `total_price` (quantity * unit_price), `date`.

### Load

5. `generate_report(transformed)` -- Generate a summary report from the transformed data. Return a dictionary with:
   - `total_revenue`: Sum of all `total_price` values (float)
   - `top_customer`: Name of the customer with the highest total spending (string)
   - `orders_per_product`: Dictionary mapping product name to count of orders for that product

## Data Formats

- `setup/customers.csv`: CSV with header row `id,name,email`
- `setup/orders.json`: JSON array of order objects
- `setup/products.xml`: XML file with `<products>` root and `<product>` children, each containing `<id>`, `<name>`, `<price>` elements

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules (csv, json, xml.etree.ElementTree)
- Do not use pandas or other external libraries
- Prices should be treated as floats
