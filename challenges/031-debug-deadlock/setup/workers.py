"""Multi-threaded worker system with shared accounts."""

import threading


lock_x = threading.Lock()
lock_y = threading.Lock()

account_x = 1000
account_y = 1000


def reset_accounts():
    """Reset accounts to initial state."""
    global account_x, account_y
    account_x = 1000
    account_y = 1000


class WorkerA(threading.Thread):
    """Transfers amount from account_x to account_y."""

    def __init__(self, amount, iterations=100):
        super().__init__()
        self.amount = amount
        self.iterations = iterations

    def run(self):
        global account_x, account_y
        for _ in range(self.iterations):
            with lock_x:
                with lock_y:
                    if account_x >= self.amount:
                        account_x -= self.amount
                        account_y += self.amount


class WorkerB(threading.Thread):
    """Transfers amount from account_y to account_x."""

    def __init__(self, amount, iterations=100):
        super().__init__()
        self.amount = amount
        self.iterations = iterations

    def run(self):
        global account_x, account_y
        for _ in range(self.iterations):
            with lock_y:
                with lock_x:
                    if account_y >= self.amount:
                        account_y -= self.amount
                        account_x += self.amount


def run_workers(amount=10, iterations=100):
    """Run both workers and return final account balances.

    Args:
        amount: Amount to transfer per iteration
        iterations: Number of transfer iterations per worker

    Returns:
        Dict with 'account_x' and 'account_y' final balances
    """
    reset_accounts()

    worker_a = WorkerA(amount, iterations)
    worker_b = WorkerB(amount, iterations)

    worker_a.start()
    worker_b.start()

    worker_a.join()
    worker_b.join()

    return {"account_x": account_x, "account_y": account_y}
