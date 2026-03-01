import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Expected trace for the 20 events:
# 1. submit: idle -> processing (transitioned)
# 2. validate: processing -> validating (transitioned)
# 3. approve(5000, lte 10000): validating -> approved (transitioned)
# 4. finalize: approved -> completed (transitioned)
# 5. reset: completed -> idle (transitioned)
# 6. submit: idle -> processing (transitioned)
# 7. error_occurred: processing -> error (transitioned)
# 8. retry: error -> processing (transitioned)
# 9. validate: processing -> validating (transitioned)
# 10. approve(15000, gt 10000): validating -> rejected (transitioned, guard: amount > 10000)
# 11. resubmit: rejected -> idle (transitioned)
# 12. submit: idle -> processing (transitioned)
# 13. finalize: processing -> processing (ignored, no transition for finalize from processing)
# 14. validate: processing -> validating (transitioned)
# 15. reject: validating -> rejected (transitioned)
# 16. resubmit: rejected -> idle (transitioned)
# 17. submit: idle -> processing (transitioned)
# 18. validate: processing -> validating (transitioned)
# 19. approve(8000, lte 10000): validating -> approved (transitioned)
# 20. finalize: approved -> completed (transitioned)

EXPECTED_FINAL_STATE = "completed"
EXPECTED_TOTAL_EVENTS = 20
EXPECTED_TRANSITIONS = 19  # 19 transitions + 1 ignored
EXPECTED_IGNORED = 1

def test_execution_trace_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "execution_trace.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "execution_trace_exists", "passed": False, "message": "execution_trace.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "execution_trace_exists", "passed": True, "message": "execution_trace.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "execution_trace_exists", "passed": False, "message": "execution_trace.json is not valid JSON"}))
        return None

def test_initial_and_final_state(data):
    if data is None:
        print(json.dumps({"test": "initial_and_final_state", "passed": False, "message": "No data to check"}))
        return
    initial = data.get("initial_state")
    final = data.get("final_state")
    if initial != "idle":
        print(json.dumps({"test": "initial_and_final_state", "passed": False, "message": f"Initial state should be 'idle', got '{initial}'"}))
        return
    if final != EXPECTED_FINAL_STATE:
        print(json.dumps({"test": "initial_and_final_state", "passed": False, "message": f"Final state should be '{EXPECTED_FINAL_STATE}', got '{final}'"}))
        return
    print(json.dumps({"test": "initial_and_final_state", "passed": True, "message": "Initial state is 'idle' and final state is 'completed'"}))

def test_total_events(data):
    if data is None:
        print(json.dumps({"test": "total_events", "passed": False, "message": "No data to check"}))
        return
    total = data.get("total_events", 0)
    transitions = data.get("transitions", [])
    if total != EXPECTED_TOTAL_EVENTS:
        print(json.dumps({"test": "total_events", "passed": False, "message": f"Expected {EXPECTED_TOTAL_EVENTS} total events, got {total}"}))
        return
    if len(transitions) != EXPECTED_TOTAL_EVENTS:
        print(json.dumps({"test": "total_events", "passed": False, "message": f"Expected {EXPECTED_TOTAL_EVENTS} transition entries, got {len(transitions)}"}))
        return
    print(json.dumps({"test": "total_events", "passed": True, "message": f"Correct number of events: {total}"}))

def test_guard_condition_handling(data):
    if data is None or "transitions" not in data:
        print(json.dumps({"test": "guard_conditions", "passed": False, "message": "No transitions to check"}))
        return
    transitions = data["transitions"]
    # Event 3 (step 3): approve with amount=5000, should go to approved (lte 10000)
    # Event 10 (step 10): approve with amount=15000, should go to rejected (gt 10000)
    step3 = next((t for t in transitions if t.get("step") == 3), None)
    step10 = next((t for t in transitions if t.get("step") == 10), None)
    if step3 is None or step10 is None:
        print(json.dumps({"test": "guard_conditions", "passed": False, "message": "Missing step 3 or step 10 in transitions"}))
        return
    if step3.get("to_state") != "approved":
        print(json.dumps({"test": "guard_conditions", "passed": False, "message": f"Step 3 (approve, amount=5000) should go to 'approved', got '{step3.get('to_state')}'"}))
        return
    if step10.get("to_state") != "rejected":
        print(json.dumps({"test": "guard_conditions", "passed": False, "message": f"Step 10 (approve, amount=15000) should go to 'rejected', got '{step10.get('to_state')}'"}))
        return
    print(json.dumps({"test": "guard_conditions", "passed": True, "message": "Guard conditions correctly applied: amount<=10000 -> approved, amount>10000 -> rejected"}))

def test_ignored_events(data):
    if data is None or "transitions" not in data:
        print(json.dumps({"test": "ignored_events", "passed": False, "message": "No transitions to check"}))
        return
    transitions = data["transitions"]
    ignored = [t for t in transitions if t.get("status") == "ignored"]
    if len(ignored) != EXPECTED_IGNORED:
        print(json.dumps({"test": "ignored_events", "passed": False, "message": f"Expected {EXPECTED_IGNORED} ignored event(s), got {len(ignored)}"}))
        return
    # Step 13 should be ignored (finalize from processing)
    step13 = next((t for t in transitions if t.get("step") == 13), None)
    if step13 is None or step13.get("status") != "ignored":
        print(json.dumps({"test": "ignored_events", "passed": False, "message": "Step 13 (finalize from processing) should be 'ignored'"}))
        return
    print(json.dumps({"test": "ignored_events", "passed": True, "message": "Ignored events correctly identified"}))

def test_transition_chain(data):
    if data is None or "transitions" not in data:
        print(json.dumps({"test": "transition_chain", "passed": False, "message": "No transitions to check"}))
        return
    transitions = sorted(data["transitions"], key=lambda t: t.get("step", 0))
    # Verify chain: each transition's from_state must equal previous transition's to_state
    expected_from = "idle"
    for t in transitions:
        actual_from = t.get("from_state")
        if actual_from != expected_from:
            print(json.dumps({"test": "transition_chain", "passed": False, "message": f"Step {t.get('step')}: expected from_state='{expected_from}', got '{actual_from}'"}))
            return
        expected_from = t.get("to_state")
    print(json.dumps({"test": "transition_chain", "passed": True, "message": "Transition chain is valid: each step's from_state matches previous step's to_state"}))

if __name__ == "__main__":
    data = test_execution_trace_exists()
    test_initial_and_final_state(data)
    test_total_events(data)
    test_guard_condition_handling(data)
    test_ignored_events(data)
    test_transition_chain(data)
