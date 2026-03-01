import json
import os
import sys
import uuid
import importlib.util

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_generator():
    path = os.path.join(CHALLENGE_DIR, "setup", "generator.py")
    spec = importlib.util.spec_from_file_location("generator", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_importable():
    try:
        mod = _load_generator()
        if not hasattr(mod, "generate_id"):
            print(json.dumps({"test": "module_importable", "passed": False, "message": "generator.py missing generate_id function"}))
            return False
        if not hasattr(mod, "generate_batch"):
            print(json.dumps({"test": "module_importable", "passed": False, "message": "generator.py missing generate_batch function"}))
            return False
        print(json.dumps({"test": "module_importable", "passed": True, "message": "generator.py imports successfully with both functions"}))
        return True
    except Exception as e:
        print(json.dumps({"test": "module_importable", "passed": False, "message": f"Failed to import generator.py: {str(e)}"}))
        return False


def test_generate_id_deterministic():
    try:
        mod = _load_generator()
        result1 = mod.generate_id("alice")
        result2 = mod.generate_id("alice")
        if result1 != result2:
            print(json.dumps({"test": "generate_id_deterministic", "passed": False, "message": f"generate_id('alice') returned different values: '{result1}' vs '{result2}'"}))
            return
        # Verify it's a valid UUID
        try:
            uuid.UUID(result1)
        except ValueError:
            print(json.dumps({"test": "generate_id_deterministic", "passed": False, "message": f"generate_id('alice') returned invalid UUID: '{result1}'"}))
            return
        print(json.dumps({"test": "generate_id_deterministic", "passed": True, "message": f"generate_id('alice') is deterministic: '{result1}'"}))
    except Exception as e:
        print(json.dumps({"test": "generate_id_deterministic", "passed": False, "message": f"Error: {str(e)}"}))


def test_different_inputs_different_outputs():
    try:
        mod = _load_generator()
        alice_id = mod.generate_id("alice")
        bob_id = mod.generate_id("bob")
        if alice_id == bob_id:
            print(json.dumps({"test": "different_inputs_different_outputs", "passed": False, "message": f"generate_id('alice') and generate_id('bob') returned same UUID: '{alice_id}'"}))
            return
        print(json.dumps({"test": "different_inputs_different_outputs", "passed": True, "message": "Different inputs produce different UUIDs"}))
    except Exception as e:
        print(json.dumps({"test": "different_inputs_different_outputs", "passed": False, "message": f"Error: {str(e)}"}))


def test_uses_uuid5_namespace_dns():
    try:
        mod = _load_generator()
        result = mod.generate_id("alice")
        expected = str(uuid.uuid5(uuid.NAMESPACE_DNS, "alice"))
        if result != expected:
            print(json.dumps({"test": "uses_uuid5_namespace_dns", "passed": False, "message": f"generate_id('alice') = '{result}', expected uuid5(NAMESPACE_DNS, 'alice') = '{expected}'"}))
            return
        print(json.dumps({"test": "uses_uuid5_namespace_dns", "passed": True, "message": f"Correctly uses uuid5 with NAMESPACE_DNS: '{result}'"}))
    except Exception as e:
        print(json.dumps({"test": "uses_uuid5_namespace_dns", "passed": False, "message": f"Error: {str(e)}"}))


def test_generate_batch():
    try:
        mod = _load_generator()
        names = ["alice", "bob", "charlie"]
        batch = mod.generate_batch(names)
        if not isinstance(batch, dict):
            print(json.dumps({"test": "generate_batch", "passed": False, "message": f"generate_batch should return dict, got {type(batch).__name__}"}))
            return
        for name in names:
            if name not in batch:
                print(json.dumps({"test": "generate_batch", "passed": False, "message": f"generate_batch missing key '{name}'"}))
                return
            expected = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
            if batch[name] != expected:
                print(json.dumps({"test": "generate_batch", "passed": False, "message": f"generate_batch['{name}'] = '{batch[name]}', expected '{expected}'"}))
                return
        print(json.dumps({"test": "generate_batch", "passed": True, "message": "generate_batch returns correct deterministic UUIDs for all names"}))
    except Exception as e:
        print(json.dumps({"test": "generate_batch", "passed": False, "message": f"Error: {str(e)}"}))


if __name__ == "__main__":
    test_module_importable()
    test_generate_id_deterministic()
    test_different_inputs_different_outputs()
    test_uses_uuid5_namespace_dns()
    test_generate_batch()
