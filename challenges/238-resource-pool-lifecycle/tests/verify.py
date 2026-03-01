import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_allocation_log():
    path = os.path.join(CHALLENGE_DIR, "setup", "allocation_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "allocation_log", "passed": False, "message": "allocation_log.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "allocation_log", "passed": False, "message": "allocation_log.json is not valid JSON"}))
        return None
    allocs = data.get("allocations", [])
    if len(allocs) != 11:
        print(json.dumps({"test": "allocation_log", "passed": False, "message": f"Expected 11 allocation entries (for 11 requests), got {len(allocs)}"}))
        return data
    # req-011 requests 32 CPU / 128 GB which exceeds all resources - must be denied
    req11 = next((a for a in allocs if a.get("request_id") == "req-011"), None)
    if req11 is None:
        print(json.dumps({"test": "allocation_log", "passed": False, "message": "req-011 not found in allocation log"}))
        return data
    if req11.get("status") != "denied":
        print(json.dumps({"test": "allocation_log", "passed": False, "message": f"req-011 (32 CPU, 128GB) should be denied, got '{req11.get('status')}'"}))
        return data
    allocated = [a for a in allocs if a.get("status") == "allocated"]
    denied = [a for a in allocs if a.get("status") == "denied"]
    # At least req-011 should be denied; depending on best-fit, some others may too
    if len(denied) < 1:
        print(json.dumps({"test": "allocation_log", "passed": False, "message": "At least 1 request should be denied (req-011 exceeds pool capacity)"}))
        return data
    print(json.dumps({"test": "allocation_log", "passed": True, "message": f"Allocation log correct: {len(allocated)} allocated, {len(denied)} denied"}))
    return data

def test_pool_state():
    path = os.path.join(CHALLENGE_DIR, "setup", "pool_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "pool_state", "passed": False, "message": "pool_state.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "pool_state", "passed": False, "message": "pool_state.json is not valid JSON"}))
        return
    resources = data.get("resources", [])
    if len(resources) != 10:
        print(json.dumps({"test": "pool_state", "passed": False, "message": f"Pool should have 10 resources, got {len(resources)}"}))
        return
    in_use = [r for r in resources if r.get("status") == "in_use"]
    for r in in_use:
        if not r.get("allocated_to"):
            print(json.dumps({"test": "pool_state", "passed": False, "message": f"Resource {r.get('resource_id')} is in_use but has no allocated_to"}))
            return
    print(json.dumps({"test": "pool_state", "passed": True, "message": f"Pool state valid: {len(in_use)} in use, {10 - len(in_use)} available"}))

def test_return_log():
    path = os.path.join(CHALLENGE_DIR, "setup", "return_log.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "return_log", "passed": False, "message": "return_log.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "return_log", "passed": False, "message": "return_log.json is not valid JSON"}))
        return
    returns = data.get("returns", [])
    if len(returns) != 3:
        print(json.dumps({"test": "return_log", "passed": False, "message": f"Expected 3 return entries, got {len(returns)}"}))
        return
    for r in returns:
        if r.get("status") != "returned":
            print(json.dumps({"test": "return_log", "passed": False, "message": f"Return {r.get('return_id')} should have status 'returned', got '{r.get('status')}'"}))
            return
    print(json.dumps({"test": "return_log", "passed": True, "message": "Return log correct: 3 resources returned"}))

def test_leak_report():
    path = os.path.join(CHALLENGE_DIR, "setup", "leak_report.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "leak_report", "passed": False, "message": "leak_report.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "leak_report", "passed": False, "message": "leak_report.json is not valid JSON"}))
        return
    if data.get("check_time") != "2024-01-15T12:00:00Z":
        print(json.dumps({"test": "leak_report", "passed": False, "message": f"check_time should be '2024-01-15T12:00:00Z', got '{data.get('check_time')}'"}))
        return
    leaks = data.get("leaks", [])
    detected = data.get("leaks_detected", 0)
    if detected != len(leaks):
        print(json.dumps({"test": "leak_report", "passed": False, "message": f"leaks_detected ({detected}) does not match number of leaks ({len(leaks)})"}))
        return
    # All resources allocated at ~08:00-08:45 with TTLs of 30-240 min.
    # By 12:00 (4 hours later = 240 min), resources with TTL < 240 that weren't returned are leaks.
    # Returned: inst-001 (alpha), inst-005 (gamma), inst-007 (epsilon)
    # Still in_use and need TTL check for the rest
    if detected < 1:
        print(json.dumps({"test": "leak_report", "passed": False, "message": "Expected at least 1 leak (resources past TTL at 12:00)"}))
        return
    for leak in leaks:
        if leak.get("action") != "reclaimed":
            print(json.dumps({"test": "leak_report", "passed": False, "message": f"Leak {leak.get('resource_id')} action should be 'reclaimed', got '{leak.get('action')}'"}))
            return
    print(json.dumps({"test": "leak_report", "passed": True, "message": f"Leak report correct: {detected} leaks detected and reclaimed"}))

def test_final_pool_state():
    path = os.path.join(CHALLENGE_DIR, "setup", "final_pool_state.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "final_pool_state", "passed": False, "message": "final_pool_state.json not found"}))
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"test": "final_pool_state", "passed": False, "message": "final_pool_state.json is not valid JSON"}))
        return
    if data.get("total_resources") != 10:
        print(json.dumps({"test": "final_pool_state", "passed": False, "message": f"total_resources should be 10, got {data.get('total_resources')}"}))
        return
    available = data.get("available", 0)
    in_use = data.get("in_use", 0)
    if available + in_use != 10:
        print(json.dumps({"test": "final_pool_state", "passed": False, "message": f"available ({available}) + in_use ({in_use}) should equal 10"}))
        return
    resources = data.get("resources", [])
    actual_available = len([r for r in resources if r.get("status") == "available"])
    actual_in_use = len([r for r in resources if r.get("status") == "in_use"])
    if actual_available != available:
        print(json.dumps({"test": "final_pool_state", "passed": False, "message": f"available count ({available}) does not match actual available resources ({actual_available})"}))
        return
    print(json.dumps({"test": "final_pool_state", "passed": True, "message": f"Final pool state correct: {available} available, {in_use} in use"}))

if __name__ == "__main__":
    test_allocation_log()
    test_pool_state()
    test_return_log()
    test_leak_report()
    test_final_pool_state()
