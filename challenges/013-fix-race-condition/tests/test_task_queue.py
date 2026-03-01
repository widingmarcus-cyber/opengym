"""Tests for Challenge 013: Fix the Race Condition."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from task_queue import TaskQueue, Counter


def square(x):
    """Compute square with a small delay to increase contention."""
    time.sleep(0.01)
    return x * x


def test_single_task():
    """A single task should produce one result."""
    tq = TaskQueue(num_workers=2)
    tq.submit("a", square, 5)
    tq.process_all()
    results = tq.get_results()
    assert results == {"a": 25}


def test_all_results_collected():
    """All submitted tasks should appear in results."""
    tq = TaskQueue(num_workers=4)
    for i in range(50):
        tq.submit(i, square, i)
    tq.process_all()
    results = tq.get_results()
    assert len(results) == 50
    for i in range(50):
        assert results[i] == i * i


def test_many_tasks_many_workers():
    """Stress test: 200 tasks across 8 workers should all complete."""
    tq = TaskQueue(num_workers=8)
    for i in range(200):
        tq.submit(f"task-{i}", square, i)
    tq.process_all()
    results = tq.get_results()
    assert len(results) == 200


def test_results_are_correct():
    """Each result value should match the expected computation."""
    tq = TaskQueue(num_workers=4)
    for i in range(20):
        tq.submit(i, lambda x: x + 100, i)
    tq.process_all()
    results = tq.get_results()
    for i in range(20):
        assert results[i] == i + 100


def test_counter_concurrent_increments():
    """Counter should correctly sum concurrent increments."""
    counter = Counter()
    num_threads = 10
    increments_per_thread = 100

    def do_increments():
        for _ in range(increments_per_thread):
            counter.increment(1)
            time.sleep(0.001)

    import threading
    threads = [threading.Thread(target=do_increments) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter.get_value() == num_threads * increments_per_thread


def test_no_results_before_processing():
    """Results should be empty before process_all is called."""
    tq = TaskQueue(num_workers=2)
    tq.submit("x", square, 3)
    assert tq.get_results() == {}
