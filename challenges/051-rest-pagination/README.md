# Challenge 051: REST Pagination Client

## Difficulty: Easy

## Task

Implement a client that fetches all pages from a paginated REST API. The file `setup/client.py` contains stubs that need to be completed.

## Setup

`setup/fake_api.py` provides a `PaginatedAPI` class that simulates a paginated API. Its `get_page(page)` method returns a dictionary with:
- `"items"`: a list of items for that page
- `"next_page"`: the next page number, or `None` if this is the last page
- `"total_pages"`: the total number of pages

## Requirements

Implement the following functions in `setup/client.py`:

1. `fetch_all_items(api)` — Fetch all pages from the API and return a flat list of all items across all pages.
2. `fetch_page_range(api, start, end)` — Fetch pages from `start` to `end` (inclusive) and return a flat list of all items from those pages. If `start` or `end` is out of range, only fetch valid pages.

## Rules

- Only modify files in the `setup/` directory (do not modify `fake_api.py`)
- Handle edge cases like empty APIs or invalid page ranges
- Do not fetch pages unnecessarily
