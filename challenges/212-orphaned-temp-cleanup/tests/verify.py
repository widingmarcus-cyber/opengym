import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPDIR = os.path.join(CHALLENGE_DIR, "setup", "tempdir")

ACTIVE_TEMPS = ["proc_alpha.tmp", "proc_beta.tmp", "proc_gamma.tmp"]
ACTIVE_LOCKS = ["proc_alpha.lock", "proc_beta.lock", "proc_gamma.lock"]
ORPHANED_TEMPS = ["proc_delta.tmp", "proc_epsilon.tmp"]
STALE_TEMPS = ["proc_zeta.tmp", "proc_eta.tmp"]
STALE_LOCKS = ["proc_zeta.lock", "proc_eta.lock"]


def test_orphaned_temps_removed():
    remaining = os.listdir(TEMPDIR)
    still_present = [f for f in ORPHANED_TEMPS + STALE_TEMPS if f in remaining]
    if still_present:
        print(json.dumps({"test": "orphaned_removed", "passed": False,
                          "message": f"Orphaned temp files still present: {still_present}"}))
        return
    print(json.dumps({"test": "orphaned_removed", "passed": True,
                      "message": "All orphaned temp files removed"}))


def test_stale_locks_removed():
    remaining = os.listdir(TEMPDIR)
    still_present = [f for f in STALE_LOCKS if f in remaining]
    if still_present:
        print(json.dumps({"test": "stale_locks_removed", "passed": False,
                          "message": f"Stale lock files still present: {still_present}"}))
        return
    print(json.dumps({"test": "stale_locks_removed", "passed": True,
                      "message": "All stale lock files removed"}))


def test_active_files_kept():
    remaining = os.listdir(TEMPDIR)
    expected_active = sorted(ACTIVE_TEMPS + ACTIVE_LOCKS)
    missing = [f for f in expected_active if f not in remaining]
    if missing:
        print(json.dumps({"test": "active_kept", "passed": False,
                          "message": f"Active files were incorrectly deleted: {missing}"}))
        return
    print(json.dumps({"test": "active_kept", "passed": True,
                      "message": "All active files preserved"}))


def test_correct_file_count():
    remaining = sorted(os.listdir(TEMPDIR))
    expected = sorted(ACTIVE_TEMPS + ACTIVE_LOCKS)
    if remaining != expected:
        print(json.dumps({"test": "file_count", "passed": False,
                          "message": f"Expected {len(expected)} files, got {len(remaining)}: {remaining}"}))
        return
    print(json.dumps({"test": "file_count", "passed": True,
                      "message": f"Exactly {len(expected)} active files remain"}))


def test_cleanup_manifest():
    path = os.path.join(CHALLENGE_DIR, "setup", "cleanup_manifest.json")
    if not os.path.exists(path):
        print(json.dumps({"test": "cleanup_manifest", "passed": False,
                          "message": "cleanup_manifest.json not found"}))
        return
    with open(path) as f:
        manifest = json.load(f)
    orphaned_removed = sorted(manifest.get("orphaned_temps_removed", []))
    expected_orphaned = sorted(ORPHANED_TEMPS + STALE_TEMPS)
    if orphaned_removed != expected_orphaned:
        print(json.dumps({"test": "cleanup_manifest", "passed": False,
                          "message": f"orphaned_temps_removed should be {expected_orphaned}, got {orphaned_removed}"}))
        return
    stale_removed = sorted(manifest.get("stale_locks_removed", []))
    if stale_removed != sorted(STALE_LOCKS):
        print(json.dumps({"test": "cleanup_manifest", "passed": False,
                          "message": f"stale_locks_removed should be {sorted(STALE_LOCKS)}, got {stale_removed}"}))
        return
    if manifest.get("total_removed") != 6:  # 4 temps + 2 stale locks
        print(json.dumps({"test": "cleanup_manifest", "passed": False,
                          "message": f"total_removed should be 6, got {manifest.get('total_removed')}"}))
        return
    if manifest.get("total_kept") != 6:  # 3 active temps + 3 active locks
        print(json.dumps({"test": "cleanup_manifest", "passed": False,
                          "message": f"total_kept should be 6, got {manifest.get('total_kept')}"}))
        return
    print(json.dumps({"test": "cleanup_manifest", "passed": True,
                      "message": "Cleanup manifest is correct"}))


if __name__ == "__main__":
    test_orphaned_temps_removed()
    test_stale_locks_removed()
    test_active_files_kept()
    test_correct_file_count()
    test_cleanup_manifest()
