# Challenge 238: Resource Pool Lifecycle

## Objective

Manage a resource pool across two sessions. In the first session, handle allocation requests from a finite pool of resources. In the second session, process returns, detect resource leaks, and rebalance the pool.

This is a **multi-session challenge** with 2 steps. See the `steps/` directory for per-step instructions.

## Setup

- `setup/resource_pool.json` - The initial pool of resources (10 compute instances with CPU/memory specs).
- `setup/allocation_requests.json` - Allocation requests to process in Step 1.
- `setup/return_events.json` - Return/release events to process in Step 2.

## Overall Flow

1. **Step 1**: Process allocation requests. Allocate resources from the pool, track who has what, handle cases where resources are insufficient. Write `setup/allocation_log.json` and `setup/pool_state.json`.
2. **Step 2**: Process return events, detect leaks (resources allocated but never returned and past TTL), rebalance the pool. Write `setup/return_log.json`, `setup/leak_report.json`, and `setup/final_pool_state.json`.

## Constraints

- Resources can only be allocated if they meet the request's minimum CPU and memory requirements.
- Each resource can only be allocated to one requester at a time.
- Allocation should prefer the smallest sufficient resource (best-fit).
- A leak is defined as a resource whose TTL has expired and has not been returned.
