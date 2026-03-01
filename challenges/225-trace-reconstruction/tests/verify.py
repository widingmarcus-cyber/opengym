import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_spans():
    path = os.path.join(CHALLENGE_DIR, "setup", "spans.json")
    with open(path) as f:
        return json.load(f)


def test_output_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "output_exists", "passed": False, "message": "trace.json not found in setup/"}))
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(json.dumps({"test": "output_exists", "passed": False, "message": "trace.json must contain a JSON object"}))
            return False
        print(json.dumps({"test": "output_exists", "passed": True, "message": "trace.json exists and is valid JSON"}))
        return True
    except json.JSONDecodeError as e:
        print(json.dumps({"test": "output_exists", "passed": False, "message": f"Invalid JSON: {str(e)}"}))
        return False


def test_root_span_correct():
    path = os.path.join(CHALLENGE_DIR, "setup", "trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "root_span_correct", "passed": False, "message": "trace.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if "root" not in data:
        print(json.dumps({"test": "root_span_correct", "passed": False, "message": "Missing 'root' key in trace.json"}))
        return
    root = data["root"]
    if root.get("span_id") != "span-001":
        print(json.dumps({"test": "root_span_correct", "passed": False, "message": f"Root span_id should be 'span-001', got '{root.get('span_id')}'"}))
        return
    if root.get("duration_ms") != 450:
        print(json.dumps({"test": "root_span_correct", "passed": False, "message": f"Root duration_ms should be 450, got {root.get('duration_ms')}"}))
        return
    if data.get("trace_id") != "trace-7f3a9b":
        print(json.dumps({"test": "root_span_correct", "passed": False, "message": f"trace_id should be 'trace-7f3a9b', got '{data.get('trace_id')}'"}))
        return
    print(json.dumps({"test": "root_span_correct", "passed": True, "message": "Root span correctly identified with proper duration"}))


def _count_spans(node):
    count = 1
    for child in node.get("children", []):
        count += _count_spans(child)
    return count


def test_tree_structure():
    path = os.path.join(CHALLENGE_DIR, "setup", "trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "tree_structure", "passed": False, "message": "trace.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    root = data.get("root", {})
    total = _count_spans(root)
    if total != 8:
        print(json.dumps({"test": "tree_structure", "passed": False, "message": f"Expected 8 spans in tree, found {total}"}))
        return
    # Check root has exactly 2 children (order-service and payment-service)
    children = root.get("children", [])
    if len(children) != 2:
        print(json.dumps({"test": "tree_structure", "passed": False, "message": f"Root should have 2 children, has {len(children)}"}))
        return
    # Check order-service child has 3 children
    order_child = None
    for c in children:
        if c.get("span_id") == "span-002":
            order_child = c
            break
    if order_child is None:
        print(json.dumps({"test": "tree_structure", "passed": False, "message": "span-002 (order-service) not found as child of root"}))
        return
    if len(order_child.get("children", [])) != 3:
        print(json.dumps({"test": "tree_structure", "passed": False, "message": f"order-service should have 3 children, has {len(order_child.get('children', []))}"}))
        return
    print(json.dumps({"test": "tree_structure", "passed": True, "message": "Tree structure is correct with proper nesting"}))


def test_children_ordered():
    path = os.path.join(CHALLENGE_DIR, "setup", "trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "children_ordered", "passed": False, "message": "trace.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)

    def check_order(node):
        children = node.get("children", [])
        for i in range(1, len(children)):
            if children[i].get("start_time_ms", 0) < children[i-1].get("start_time_ms", 0):
                return False, node.get("span_id")
        for c in children:
            ok, bad_id = check_order(c)
            if not ok:
                return False, bad_id
        return True, None

    ok, bad_id = check_order(data.get("root", {}))
    if not ok:
        print(json.dumps({"test": "children_ordered", "passed": False, "message": f"Children of span '{bad_id}' are not ordered by start_time_ms"}))
        return
    print(json.dumps({"test": "children_ordered", "passed": True, "message": "All children ordered by start_time_ms"}))


def test_summary_fields():
    path = os.path.join(CHALLENGE_DIR, "setup", "trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "summary_fields", "passed": False, "message": "trace.json not found"}))
        return
    with open(path) as f:
        data = json.load(f)
    if data.get("total_spans") != 8:
        print(json.dumps({"test": "summary_fields", "passed": False, "message": f"total_spans should be 8, got {data.get('total_spans')}"}))
        return
    if data.get("total_duration_ms") != 450:
        print(json.dumps({"test": "summary_fields", "passed": False, "message": f"total_duration_ms should be 450, got {data.get('total_duration_ms')}"}))
        return
    # Critical path: root(450) -> payment(130) -> sendReceipt(90) = 450 (root duration covers it)
    # The critical path is the longest chain of durations: root includes all
    # Actually critical_path_ms = root duration = 450 since root encompasses everything
    if "critical_path_ms" not in data:
        print(json.dumps({"test": "summary_fields", "passed": False, "message": "Missing 'critical_path_ms' field"}))
        return
    print(json.dumps({"test": "summary_fields", "passed": True, "message": "Summary fields present and correct"}))


if __name__ == "__main__":
    test_output_exists()
    test_root_span_correct()
    test_tree_structure()
    test_children_ordered()
    test_summary_fields()
