import json
import os
import re

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse_version(v):
    return tuple(int(x) for x in v.split("."))

def satisfies_constraint(version, constraint):
    """Check if a version string satisfies a constraint string like '>=1.0.0,<2.0.0'."""
    parts = [c.strip() for c in constraint.split(",")]
    v = parse_version(version)
    for part in parts:
        m = re.match(r'(>=|<=|>|<|==)(\d+\.\d+\.\d+)', part)
        if not m:
            return False
        op, ref = m.group(1), parse_version(m.group(2))
        if op == ">=" and not (v >= ref):
            return False
        if op == "<=" and not (v <= ref):
            return False
        if op == ">" and not (v > ref):
            return False
        if op == "<" and not (v < ref):
            return False
        if op == "==" and not (v == ref):
            return False
    return True

def test_resolution_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "resolution.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "resolution_exists", "passed": False, "message": "resolution.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "resolution_exists", "passed": True, "message": "resolution.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "resolution_exists", "passed": False, "message": "resolution.json is not valid JSON"}))
        return None

def test_all_requirements_resolved(data):
    if data is None:
        print(json.dumps({"test": "requirements_resolved", "passed": False, "message": "No resolution data"}))
        return
    if not data.get("resolved", False):
        print(json.dumps({"test": "requirements_resolved", "passed": False, "message": "Resolution reports resolved=false"}))
        return
    packages = data.get("packages", {})
    req_path = os.path.join(CHALLENGE_DIR, "setup", "requirements.json")
    with open(req_path) as f:
        reqs = json.load(f)
    for pkg, constraint in reqs["requirements"].items():
        if pkg not in packages:
            print(json.dumps({"test": "requirements_resolved", "passed": False, "message": f"Required package '{pkg}' not in resolution"}))
            return
        version = packages[pkg].get("version", "")
        if not satisfies_constraint(version, constraint):
            print(json.dumps({"test": "requirements_resolved", "passed": False, "message": f"Package '{pkg}' version {version} does not satisfy constraint {constraint}"}))
            return
    print(json.dumps({"test": "requirements_resolved", "passed": True, "message": "All top-level requirements are resolved with valid versions"}))

def test_dependency_constraints(data):
    if data is None or not data.get("resolved", False):
        print(json.dumps({"test": "dependency_constraints", "passed": False, "message": "No valid resolution to check"}))
        return
    packages = data.get("packages", {})
    pkg_path = os.path.join(CHALLENGE_DIR, "setup", "packages.json")
    with open(pkg_path) as f:
        registry = json.load(f)
    for pkg_name, pkg_info in packages.items():
        version = pkg_info.get("version", "")
        if pkg_name not in registry["packages"]:
            print(json.dumps({"test": "dependency_constraints", "passed": False, "message": f"Package '{pkg_name}' not found in registry"}))
            return
        if version not in registry["packages"][pkg_name]["versions"]:
            print(json.dumps({"test": "dependency_constraints", "passed": False, "message": f"Version {version} of '{pkg_name}' not found in registry"}))
            return
        deps = registry["packages"][pkg_name]["versions"][version].get("dependencies", {})
        for dep_name, dep_constraint in deps.items():
            if dep_name not in packages:
                print(json.dumps({"test": "dependency_constraints", "passed": False, "message": f"'{pkg_name}@{version}' depends on '{dep_name}' but it is not in resolution"}))
                return
            dep_version = packages[dep_name].get("version", "")
            if not satisfies_constraint(dep_version, dep_constraint):
                print(json.dumps({"test": "dependency_constraints", "passed": False, "message": f"'{pkg_name}@{version}' requires '{dep_name} {dep_constraint}' but got {dep_version}"}))
                return
    print(json.dumps({"test": "dependency_constraints", "passed": True, "message": "All dependency version constraints are satisfied"}))

def test_install_order_exists():
    path = os.path.join(CHALLENGE_DIR, "setup", "install_order.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "install_order_exists", "passed": False, "message": "install_order.json not found"}))
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print(json.dumps({"test": "install_order_exists", "passed": True, "message": "install_order.json exists and is valid JSON"}))
        return data
    except json.JSONDecodeError:
        print(json.dumps({"test": "install_order_exists", "passed": False, "message": "install_order.json is not valid JSON"}))
        return None

def test_topological_order(resolution, install_order):
    if resolution is None or install_order is None:
        print(json.dumps({"test": "topological_order", "passed": False, "message": "Missing resolution or install_order data"}))
        return
    packages = resolution.get("packages", {})
    order = install_order.get("order", [])
    pkg_path = os.path.join(CHALLENGE_DIR, "setup", "packages.json")
    with open(pkg_path) as f:
        registry = json.load(f)
    # Build position map
    position = {}
    for i, entry in enumerate(order):
        parts = entry.split("@")
        if len(parts) == 2:
            position[parts[0]] = i
    # Verify all resolved packages are in the order
    for pkg_name in packages:
        if pkg_name not in position:
            print(json.dumps({"test": "topological_order", "passed": False, "message": f"Package '{pkg_name}' is in resolution but not in install_order"}))
            return
    # Verify topological ordering: dependencies come before dependents
    for pkg_name, pkg_info in packages.items():
        version = pkg_info.get("version", "")
        if pkg_name not in registry["packages"] or version not in registry["packages"][pkg_name]["versions"]:
            continue
        deps = registry["packages"][pkg_name]["versions"][version].get("dependencies", {})
        for dep_name in deps:
            if dep_name in position and pkg_name in position:
                if position[dep_name] >= position[pkg_name]:
                    print(json.dumps({"test": "topological_order", "passed": False, "message": f"'{dep_name}' must be installed before '{pkg_name}' but appears later in order"}))
                    return
    print(json.dumps({"test": "topological_order", "passed": True, "message": "Install order is a valid topological sort"}))

def test_no_duplicate_packages(resolution):
    if resolution is None:
        print(json.dumps({"test": "no_duplicates", "passed": False, "message": "No resolution data"}))
        return
    packages = resolution.get("packages", {})
    # Each package should appear only once
    if len(packages) != resolution.get("total_packages", -1):
        print(json.dumps({"test": "no_duplicates", "passed": False, "message": f"total_packages ({resolution.get('total_packages')}) does not match number of packages ({len(packages)})"}))
        return
    print(json.dumps({"test": "no_duplicates", "passed": True, "message": f"No duplicate packages; {len(packages)} unique packages resolved"}))

if __name__ == "__main__":
    resolution = test_resolution_exists()
    test_all_requirements_resolved(resolution)
    test_dependency_constraints(resolution)
    install_order = test_install_order_exists()
    test_topological_order(resolution, install_order)
    test_no_duplicate_packages(resolution)
