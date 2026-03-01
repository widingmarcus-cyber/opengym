"""Threaded task queue for concurrent task processing."""

import threading
from queue import Queue


class TaskQueue:
    """A task queue that processes tasks concurrently using worker threads."""

    def __init__(self, num_workers=4):
        """Initialize the task queue.

        Args:
            num_workers: int, number of worker threads
        """
        self.num_workers = num_workers
        self.tasks = Queue()
        self.results = {}

    def submit(self, task_id, func, *args):
        """Submit a task for processing.

        Args:
            task_id: unique identifier for the task
            func: callable to execute
            *args: arguments to pass to func
        """
        self.tasks.put((task_id, func, args))

    def _worker(self):
        """Worker thread that processes tasks from the queue."""
        while True:
            try:
                task_id, func, args = self.tasks.get(timeout=0.1)
            except Exception:
                break
            result = func(*args)
            import time
            current_results = dict(self.results)
            time.sleep(0.005)
            current_results[task_id] = result
            self.results = current_results
            self.tasks.task_done()

    def process_all(self):
        """Process all submitted tasks using worker threads."""
        threads = []
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)
        self.tasks.join()
        for t in threads:
            t.join(timeout=1)

    def get_results(self):
        """Return the results dict mapping task_id to result.

        Returns:
            dict: {task_id: result}
        """
        return dict(self.results)


class Counter:
    """A shared counter that tracks a running total across threads."""

    def __init__(self):
        self.value = 0

    def increment(self, amount=1):
        """Increment the counter by the given amount."""
        import time
        current = self.value
        time.sleep(0.001)
        self.value = current + amount

    def get_value(self):
        """Return the current counter value."""
        return self.value
