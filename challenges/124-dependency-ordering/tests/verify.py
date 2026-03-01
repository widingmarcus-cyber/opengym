#!/usr/bin/env python3
"""Verify Challenge 124: Dependency Ordering — all tasks executed in correct DAG order."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(CHALLENGE_DIR, "setup", "outputs")
MANIFEST_PATH = os.path.join(CHALLENGE_DIR, "setup", "build_manifest.json")
TASKS_PATH = os.path.join(CHALLENGE_DIR, "setup", "build_tasks.json")

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def read_file(name):
    path = os.path.join(OUTPUTS_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read().strip()


def main():
    # Check all 8 output files exist
    expected_files = [
        "core.txt", "utils.txt", "api.txt", "auth.txt",
        "backend.txt", "frontend.txt", "app.txt", "package.txt",
    ]
    all_exist = all(
        os.path.exists(os.path.join(OUTPUTS_DIR, f)) for f in expected_files
    )
    missing = [f for f in expected_files if not os.path.exists(os.path.join(OUTPUTS_DIR, f))]
    check(
        "all_output_files_exist",
        all_exist,
        f"Missing files: {missing}" if missing else "All 8 output files exist",
    )

    # Check core.txt
    core = read_file("core.txt")
    check(
        "core_content",
        core is not None and "core_v1" in core,
        f"core.txt content: {core}",
    )

    # Check api.txt contains core_v1 and api
    api = read_file("api.txt")
    check(
        "api_content",
        api is not None and "core_v1" in api and "api" in api.lower(),
        f"api.txt content: {api}",
    )

    # Check auth.txt contains core_v1, utils_v1, and auth
    auth = read_file("auth.txt")
    check(
        "auth_content",
        auth is not None and "core_v1" in auth and "utils_v1" in auth and "auth" in auth.lower(),
        f"auth.txt content: {auth}",
    )

    # Check backend.txt contains content from api and auth
    backend = read_file("backend.txt")
    has_api = backend is not None and ("api" in backend.lower())
    has_auth = backend is not None and ("auth" in backend.lower())
    check(
        "backend_content",
        has_api and has_auth,
        f"backend.txt content: {backend}",
    )

    # Check app.txt contains content from backend and frontend
    app = read_file("app.txt")
    has_backend = app is not None and ("backend" in app.lower() or "api" in app.lower())
    has_frontend = app is not None and ("frontend" in app.lower())
    check(
        "app_content",
        has_backend and has_frontend,
        f"app.txt content: {app}",
    )

    # Check package.txt has PACKAGE wrapper
    package = read_file("package.txt")
    check(
        "package_content",
        package is not None and "PACKAGE" in package,
        f"package.txt content: {package}",
    )

    # Check build_manifest.json exists and has valid ordering
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r") as f:
                manifest = json.load(f)

            # Extract the execution order list
            order = None
            if isinstance(manifest, list):
                order = manifest
            elif isinstance(manifest, dict):
                # Try common keys
                for key in ["order", "execution_order", "steps", "tasks"]:
                    if key in manifest and isinstance(manifest[key], list):
                        order = manifest[key]
                        break

            if order is None:
                check("manifest_valid_order", False, "Could not find execution order list in manifest")
            else:
                # Load task definitions for dependency checking
                with open(TASKS_PATH, "r") as f:
                    tasks_data = json.load(f)
                deps = {
                    name: info["depends_on"]
                    for name, info in tasks_data["tasks"].items()
                }

                # Verify all tasks are in the order
                all_tasks = set(deps.keys())
                order_set = set(order)
                all_present = all_tasks.issubset(order_set)

                # Verify dependencies come before dependents
                valid_order = True
                seen = set()
                for task in order:
                    if task in deps:
                        for dep in deps[task]:
                            if dep not in seen:
                                valid_order = False
                                break
                    seen.add(task)

                check(
                    "manifest_valid_order",
                    all_present and valid_order,
                    f"Order: {order}, all present: {all_present}, valid: {valid_order}",
                )
        except json.JSONDecodeError as e:
            check("manifest_valid_order", False, f"Invalid JSON in manifest: {e}")
    else:
        check("manifest_valid_order", False, "build_manifest.json not found")

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
