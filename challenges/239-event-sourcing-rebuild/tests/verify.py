import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Expected final state after replaying all 25 events:
# Users: user-001 (active, email updated), user-002 (active, role=moderator), user-003 (deleted), user-004 (active)
# Products: prod-001 (active, stock=92), prod-002 (active, price=39.99, stock=49), prod-003 (active, stock=23), prod-004 (deleted)
# Orders: order-001 (delivered), order-002 (shipped), order-003 (cancelled), order-004 (pending)

def test_current_state_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "current_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "current_state_exists", "passed": False, "message": "current_state.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "current_state_exists", "passed": True, "message": "current_state.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "current_state_exists", "passed": False, "message": "current_state.json is not valid JSON"}))
        return None

def test_users_state(data):
    if data is None:
        print(json.dumps({"test": "users_state", "passed": False, "message": "No data to check"}))
        return
    users = data.get("users", {})
    # user-003 was deleted, should not be present
    if "user-003" in users:
        print(json.dumps({"test": "users_state", "passed": False, "message": "user-003 was deleted but still appears in current state"}))
        return
    expected_active = {"user-001", "user-002", "user-004"}
    if set(users.keys()) != expected_active:
        print(json.dumps({"test": "users_state", "passed": False, "message": f"Expected active users {expected_active}, got {set(users.keys())}"}))
        return
    # user-001 email should be updated
    if users.get("user-001", {}).get("email") != "alice.johnson@example.com":
        print(json.dumps({"test": "users_state", "passed": False, "message": f"user-001 email should be 'alice.johnson@example.com', got '{users.get('user-001', {}).get('email')}'"}))
        return
    # user-002 role should be moderator
    if users.get("user-002", {}).get("role") != "moderator":
        print(json.dumps({"test": "users_state", "passed": False, "message": f"user-002 role should be 'moderator', got '{users.get('user-002', {}).get('role')}'"}))
        return
    print(json.dumps({"test": "users_state", "passed": True, "message": "Users state is correct: 3 active, 1 deleted, updates applied"}))

def test_products_state(data):
    if data is None:
        print(json.dumps({"test": "products_state", "passed": False, "message": "No data to check"}))
        return
    products = data.get("products", {})
    # prod-004 was deleted
    if "prod-004" in products:
        print(json.dumps({"test": "products_state", "passed": False, "message": "prod-004 was deleted but still appears in current state"}))
        return
    expected_active = {"prod-001", "prod-002", "prod-003"}
    if set(products.keys()) != expected_active:
        print(json.dumps({"test": "products_state", "passed": False, "message": f"Expected active products {expected_active}, got {set(products.keys())}"}))
        return
    # prod-001 stock should be 92
    if products.get("prod-001", {}).get("stock") != 92:
        print(json.dumps({"test": "products_state", "passed": False, "message": f"prod-001 stock should be 92, got {products.get('prod-001', {}).get('stock')}"}))
        return
    # prod-002 price should be 39.99 and stock 49
    p2 = products.get("prod-002", {})
    if p2.get("price") != 39.99:
        print(json.dumps({"test": "products_state", "passed": False, "message": f"prod-002 price should be 39.99, got {p2.get('price')}"}))
        return
    if p2.get("stock") != 49:
        print(json.dumps({"test": "products_state", "passed": False, "message": f"prod-002 stock should be 49, got {p2.get('stock')}"}))
        return
    print(json.dumps({"test": "products_state", "passed": True, "message": "Products state is correct: 3 active, 1 deleted, updates applied"}))

def test_orders_state(data):
    if data is None:
        print(json.dumps({"test": "orders_state", "passed": False, "message": "No data to check"}))
        return
    orders = data.get("orders", {})
    expected_orders = {"order-001", "order-002", "order-003", "order-004"}
    if set(orders.keys()) != expected_orders:
        print(json.dumps({"test": "orders_state", "passed": False, "message": f"Expected orders {expected_orders}, got {set(orders.keys())}"}))
        return
    status_checks = {
        "order-001": "delivered",
        "order-002": "shipped",
        "order-003": "cancelled",
        "order-004": "pending"
    }
    for oid, expected_status in status_checks.items():
        actual = orders.get(oid, {}).get("status")
        if actual != expected_status:
            print(json.dumps({"test": "orders_state", "passed": False, "message": f"{oid} status should be '{expected_status}', got '{actual}'"}))
            return
    print(json.dumps({"test": "orders_state", "passed": True, "message": "Orders state is correct: all 4 orders with correct statuses"}))

def test_replay_summary():
    path = os.path.join(CHALLENGE_DIR, "setup", "replay_summary.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "replay_summary", "passed": False, "message": "replay_summary.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "replay_summary", "passed": False, "message": "replay_summary.json is not valid JSON"}))
        return
    if data.get("total_events") != 25:
        print(json.dumps({"test": "replay_summary", "passed": False, "message": f"total_events should be 25, got {data.get('total_events')}"}))
        return
    by_type = data.get("events_by_type", {})
    # 9 creates, 12 updates (including 1 ignored update to deleted user-003), 2 deletes (+ 2 = 25... let me recount)
    # Actually: creates = seq 1,2,3,4,5,6,9,10,18,21,22 = 11; updates = seq 7,8,11,12,14,16,17,19,23,24,25 = 11; deletes = seq 15,20 = 2 (total not 25)
    # Wait: 11+11+2 = 24, but there are 25 events. Let me recount.
    # seq 13 = create order-003. So creates: 1,2,3,4,5,6,9,10,13,18,21,22 = 12; updates: 7,8,11,12,14,16,17,19,23,24,25 = 11; deletes: 15,20 = 2. Total: 12+11+2=25. Correct.
    expected_by_type = {"create": 12, "update": 11, "delete": 2}
    for etype, expected_count in expected_by_type.items():
        actual = by_type.get(etype, 0)
        if actual != expected_count:
            print(json.dumps({"test": "replay_summary", "passed": False, "message": f"events_by_type['{etype}'] should be {expected_count}, got {actual}"}))
            return
    print(json.dumps({"test": "replay_summary", "passed": True, "message": "Replay summary is correct: 25 events (12 create, 11 update, 2 delete)"}))

def test_deleted_entity_update_ignored(data):
    if data is None:
        print(json.dumps({"test": "deleted_update_ignored", "passed": False, "message": "No data to check"}))
        return
    users = data.get("users", {})
    # Event seq 16 tries to update deleted user-003; it should be ignored
    # user-003 should still not exist
    if "user-003" in users:
        print(json.dumps({"test": "deleted_update_ignored", "passed": False, "message": "user-003 was deleted at seq 15 and update at seq 16 should be ignored, but user-003 exists in state"}))
        return
    print(json.dumps({"test": "deleted_update_ignored", "passed": True, "message": "Update to deleted entity (user-003 at seq 16) correctly ignored"}))

if __name__ == "__main__":
    data = test_current_state_exists()
    test_users_state(data)
    test_products_state(data)
    test_orders_state(data)
    test_replay_summary()
    test_deleted_entity_update_ignored(data)
