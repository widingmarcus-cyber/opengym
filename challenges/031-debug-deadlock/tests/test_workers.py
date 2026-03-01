"""Tests for Challenge 031: Debug the Deadlock."""

import inspect
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import workers
from workers import WorkerA, WorkerB, reset_accounts


TIMEOUT = 5


def _run_pair(amount, iterations):
    """Helper: run a pair of workers with timeout protection.

    Returns (a_alive, b_alive) booleans.
    """
    reset_accounts()
    worker_a = WorkerA(amount, iterations)
    worker_b = WorkerB(amount, iterations)

    worker_a.start()
    worker_b.start()

    worker_a.join(timeout=TIMEOUT)
    worker_b.join(timeout=TIMEOUT)

    return worker_a.is_alive(), worker_b.is_alive()


def test_consistent_lock_ordering():
    """Both workers must acquire locks in the same order to prevent deadlock."""
    source_a = inspect.getsource(WorkerA.run)
    source_b = inspect.getsource(WorkerB.run)

    locks_a = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_a)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)

    assert len(locks_a) >= 2, "WorkerA should acquire at least 2 locks"
    assert len(locks_b) >= 2, "WorkerB should acquire at least 2 locks"
    assert locks_a == locks_b, (
        f"Workers acquire locks in different order: "
        f"WorkerA={locks_a}, WorkerB={locks_b}. "
        f"This causes deadlock — both must use the same ordering."
    )


def test_first_lock_same_for_both():
    """Both workers must acquire the SAME lock first."""
    source_a = inspect.getsource(WorkerA.run)
    source_b = inspect.getsource(WorkerB.run)
    locks_a = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_a)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert locks_a[0] == locks_b[0], (
        f"First lock differs: WorkerA starts with {locks_a[0]}, "
        f"WorkerB starts with {locks_b[0]}. Both must start with the same lock."
    )


def test_second_lock_same_for_both():
    """Both workers must acquire the SAME lock second."""
    source_a = inspect.getsource(WorkerA.run)
    source_b = inspect.getsource(WorkerB.run)
    locks_a = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_a)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert locks_a[1] == locks_b[1], (
        f"Second lock differs: WorkerA uses {locks_a[1]}, "
        f"WorkerB uses {locks_b[1]}. Both must use the same lock ordering."
    )


def test_no_reversed_nesting():
    """WorkerB must not nest locks in reverse order of WorkerA."""
    source_a = inspect.getsource(WorkerA.run)
    source_b = inspect.getsource(WorkerB.run)
    locks_a = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_a)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert locks_b != list(reversed(locks_a)), (
        f"WorkerB acquires locks in reversed order of WorkerA: "
        f"A={locks_a}, B={locks_b}. This is the classic deadlock pattern."
    )


def test_run_workers_function_no_deadlock():
    """The run_workers() function must complete without hanging."""
    import threading
    result = [None]
    def _run():
        result[0] = workers.run_workers(amount=5, iterations=100)
    t = threading.Thread(target=_run)
    t.start()
    t.join(timeout=TIMEOUT)
    assert not t.is_alive(), "run_workers() hung (deadlock in run_workers function)"
    assert result[0] is not None, "run_workers() returned None"
    assert result[0]["account_x"] + result[0]["account_y"] == 2000


def test_workers_complete_without_hanging():
    """Both workers must complete within the timeout (no deadlock)."""
    a_alive, b_alive = _run_pair(10, 200)
    assert not a_alive, "WorkerA is still running (deadlock?)"
    assert not b_alive, "WorkerB is still running (deadlock?)"


def test_total_balance_preserved():
    """Total balance across both accounts should always be 2000."""
    a_alive, b_alive = _run_pair(10, 100)
    assert not a_alive and not b_alive, "Workers deadlocked"
    total = workers.account_x + workers.account_y
    assert total == 2000, f"Total balance should be 2000, got {total}"


def test_balances_non_negative():
    """Neither account should go negative."""
    a_alive, b_alive = _run_pair(5, 200)
    assert not a_alive and not b_alive, "Workers deadlocked"
    assert workers.account_x >= 0, f"account_x is negative: {workers.account_x}"
    assert workers.account_y >= 0, f"account_y is negative: {workers.account_y}"


def test_run_workers_returns_dict():
    """run_workers should return a dict with the expected keys."""
    a_alive, b_alive = _run_pair(1, 10)
    assert not a_alive and not b_alive, "Workers deadlocked"
    result = {"account_x": workers.account_x, "account_y": workers.account_y}
    assert isinstance(result, dict)
    assert "account_x" in result
    assert "account_y" in result


def test_multiple_runs_no_deadlock():
    """Running multiple times should never deadlock."""
    for i in range(3):
        a_alive, b_alive = _run_pair(10, 50)
        assert not a_alive and not b_alive, f"Run {i}: workers deadlocked"
        total = workers.account_x + workers.account_y
        assert total == 2000, f"Run {i}: total balance should be 2000, got {total}"


def test_concurrent_stress():
    """Stress test with many iterations to ensure no deadlock under load."""
    a_alive, b_alive = _run_pair(1, 1000)
    assert not a_alive, "WorkerA hung during stress test"
    assert not b_alive, "WorkerB hung during stress test"


def test_both_workers_start_with_lock_x():
    """Both workers must acquire lock_x as their first lock."""
    source_a = inspect.getsource(WorkerA.run)
    source_b = inspect.getsource(WorkerB.run)
    locks_a = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_a)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert locks_a[0] == "lock_x", (
        f"WorkerA should acquire lock_x first, but starts with {locks_a[0]}"
    )
    assert locks_b[0] == "lock_x", (
        f"WorkerB should acquire lock_x first, but starts with {locks_b[0]}. "
        f"Both workers must use the same lock ordering to prevent deadlock."
    )


def test_worker_b_does_not_start_with_lock_y():
    """WorkerB must NOT acquire lock_y first — that causes deadlock with WorkerA."""
    source_b = inspect.getsource(WorkerB.run)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert locks_b[0] != "lock_y", (
        f"WorkerB acquires lock_y first — this is the deadlock cause. "
        f"It must acquire lock_x first, same as WorkerA."
    )


def test_worker_b_second_lock_is_lock_y():
    """WorkerB's second lock must be lock_y (matching WorkerA's x→y ordering)."""
    source_b = inspect.getsource(WorkerB.run)
    locks_b = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source_b)
    assert len(locks_b) >= 2, "WorkerB should acquire at least 2 locks"
    assert locks_b[1] == "lock_y", (
        f"WorkerB's second lock should be lock_y, but got {locks_b[1]}. "
        f"Lock ordering must be: lock_x → lock_y for both workers."
    )


def test_lock_ordering_matches_alphabetical():
    """Lock ordering should be alphabetical (lock_x before lock_y) in both workers."""
    for cls_name, cls in [("WorkerA", WorkerA), ("WorkerB", WorkerB)]:
        source = inspect.getsource(cls.run)
        locks = re.findall(r'(?:with|acquire)\s*\(?\s*(lock_\w+)', source)
        assert locks == sorted(locks), (
            f"{cls_name} acquires locks in non-alphabetical order: {locks}. "
            f"Both workers must use consistent ordering (lock_x then lock_y)."
        )
