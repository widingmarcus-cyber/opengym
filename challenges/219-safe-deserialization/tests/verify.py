import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from loader import load_config, parse_user_input, load_message


def test_load_config_with_json():
    """load_config should work with JSON-encoded bytes."""
    data = b'{"database": "mydb", "port": 5432}'
    result = load_config(data)
    if result.get("status") != "ok":
        print(json.dumps({"test": "load_config_with_json", "passed": False,
                          "message": f"load_config failed with JSON bytes: {result}"}))
        return
    expected = {"database": "mydb", "port": 5432}
    if result.get("data") != expected:
        print(json.dumps({"test": "load_config_with_json", "passed": False,
                          "message": f"Expected {expected}, got: {result.get('data')}"}))
        return
    print(json.dumps({"test": "load_config_with_json", "passed": True, "message": "OK"}))


def test_no_pickle_in_source():
    """The source code must not use pickle.loads anywhere."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "loader.py")
    with open(source_path, "r") as f:
        source = f.read()
    if "pickle.loads" in source or "pickle.load(" in source:
        print(json.dumps({"test": "no_pickle_in_source", "passed": False,
                          "message": "loader.py still uses pickle.loads — must use json.loads instead"}))
        return
    if "import pickle" in source:
        print(json.dumps({"test": "no_pickle_in_source", "passed": False,
                          "message": "loader.py still imports pickle — remove it"}))
        return
    print(json.dumps({"test": "no_pickle_in_source", "passed": True, "message": "OK"}))


def test_no_eval_in_source():
    """The source code must not use eval() for parsing."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "loader.py")
    with open(source_path, "r") as f:
        source = f.read()
    # Check for bare eval( but not literal_eval(
    lines = source.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "eval(" in stripped and "literal_eval(" not in stripped:
            print(json.dumps({"test": "no_eval_in_source", "passed": False,
                              "message": f"loader.py still uses eval(): '{stripped}'"}))
            return
    print(json.dumps({"test": "no_eval_in_source", "passed": True, "message": "OK"}))


def test_parse_user_input_works():
    """parse_user_input should work with Python literal strings."""
    result = parse_user_input("{'name': 'Alice', 'age': 30}")
    if result.get("status") != "ok":
        print(json.dumps({"test": "parse_user_input_works", "passed": False,
                          "message": f"parse_user_input failed: {result}"}))
        return
    data = result.get("data")
    if data != {"name": "Alice", "age": 30}:
        print(json.dumps({"test": "parse_user_input_works", "passed": False,
                          "message": f"Expected dict with Alice, got: {data}"}))
        return
    print(json.dumps({"test": "parse_user_input_works", "passed": True, "message": "OK"}))


def test_load_message_still_works():
    """load_message (already safe) must still function correctly."""
    result = load_message('{"msg": "hello", "count": 42}')
    if result.get("status") != "ok":
        print(json.dumps({"test": "load_message_still_works", "passed": False,
                          "message": f"load_message broke: {result}"}))
        return
    data = result.get("data")
    if data != {"msg": "hello", "count": 42}:
        print(json.dumps({"test": "load_message_still_works", "passed": False,
                          "message": f"Expected correct data, got: {data}"}))
        return
    print(json.dumps({"test": "load_message_still_works", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_load_config_with_json()
    test_no_pickle_in_source()
    test_no_eval_in_source()
    test_parse_user_input_works()
    test_load_message_still_works()
