"""Build script that processes source files and produces a build manifest.

WARNING: This script is NON-DETERMINISTIC. Running it twice produces
different output hashes. Your task is to fix all sources of non-determinism.
"""

import hashlib
import json
import os
import random
import datetime


def build():
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_output.json")

    files = {}
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                files[filename] = f.read()

    metadata = {
        "build_timestamp": datetime.datetime.now().isoformat(),
        "build_id": f"build-{random.random()}",
        "build_directory": os.getcwd(),
        "file_count": len(files),
    }

    # Create manifest
    manifest = {
        "metadata": metadata,
        "files": files,
    }

    # Compute hash of manifest
    manifest_json = json.dumps(manifest)
    manifest["hash"] = hashlib.sha256(manifest_json.encode()).hexdigest()

    # Write output
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Build complete. Hash: {manifest['hash']}")
    return manifest


if __name__ == "__main__":
    build()
