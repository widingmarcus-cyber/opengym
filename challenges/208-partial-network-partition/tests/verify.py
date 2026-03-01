import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_merged_data_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "merged_data.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "merged_exists", "passed": False, "message": "merged_data.json not found"}))
        return
    print(json.dumps({"test": "merged_exists", "passed": True, "message": "merged_data.json exists"}))


def test_merged_has_all_sections():
    path = os.path.join(CHALLENGE_DIR, "setup", "merged_data.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "all_sections", "passed": False, "message": "merged_data.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    required = ["users", "orders", "products", "inventory"]
    for section in required:
        if section not in data:
            print(json.dumps({"test": "all_sections", "passed": False,
                              "message": f"merged_data.json missing section '{section}'"}))
            return
    print(json.dumps({"test": "all_sections", "passed": True, "message": "All 4 data sections present"}))


def test_reconstructed_orders():
    path = os.path.join(CHALLENGE_DIR, "setup", "merged_data.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "orders_reconstructed", "passed": False, "message": "merged_data.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    orders = data.get("orders", [])
    if len(orders) != 5:
        print(json.dumps({"test": "orders_reconstructed", "passed": False,
                          "message": f"Should have 5 orders, got {len(orders)}"}))
        return
    order_ids = sorted([o.get("order_id") for o in orders])
    if order_ids != ["O1", "O2", "O3", "O4", "O5"]:
        print(json.dumps({"test": "orders_reconstructed", "passed": False,
                          "message": f"Order IDs should be O1-O5, got {order_ids}"}))
        return
    print(json.dumps({"test": "orders_reconstructed", "passed": True, "message": "All 5 orders reconstructed"}))


def test_reconstructed_inventory():
    path = os.path.join(CHALLENGE_DIR, "setup", "merged_data.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "inventory_reconstructed", "passed": False, "message": "merged_data.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    inv = data.get("inventory", [])
    if len(inv) != 3:
        print(json.dumps({"test": "inventory_reconstructed", "passed": False,
                          "message": f"Should have 3 inventory items, got {len(inv)}"}))
        return
    for item in inv:
        if "quantity_in_stock" not in item or "warehouse" not in item:
            print(json.dumps({"test": "inventory_reconstructed", "passed": False,
                              "message": f"Inventory item missing required fields: {item}"}))
            return
    print(json.dumps({"test": "inventory_reconstructed", "passed": True,
                      "message": "All 3 inventory items reconstructed"}))


def test_partition_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "partition_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "partition_report", "passed": False, "message": "partition_report.json not found"}))
        return
    with open(path) as f:
        report = json.load(f)
    if sorted(report.get("endpoints_up", [])) != ["products", "users"]:
        print(json.dumps({"test": "partition_report", "passed": False,
                          "message": f"endpoints_up should be ['products','users'], got {report.get('endpoints_up')}"}))
        return
    if sorted(report.get("endpoints_down", [])) != ["inventory", "orders"]:
        print(json.dumps({"test": "partition_report", "passed": False,
                          "message": f"endpoints_down should be ['inventory','orders'], got {report.get('endpoints_down')}"}))
        return
    total = report.get("total_records", 0)
    if total != 14:  # 3 users + 5 orders + 3 products + 3 inventory
        print(json.dumps({"test": "partition_report", "passed": False,
                          "message": f"total_records should be 14, got {total}"}))
        return
    print(json.dumps({"test": "partition_report", "passed": True, "message": "Partition report is valid"}))


if __name__ == "__main__":
    test_merged_data_exists()
    test_merged_has_all_sections()
    test_reconstructed_orders()
    test_reconstructed_inventory()
    test_partition_report()
