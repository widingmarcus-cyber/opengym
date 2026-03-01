class PaginatedAPI:
    """Simulated paginated API."""

    def __init__(self, items, page_size=3):
        self._items = list(items)
        self._page_size = page_size
        self._total_pages = max(1, (len(self._items) + page_size - 1) // page_size)
        if len(self._items) == 0:
            self._total_pages = 0

    def get_page(self, page):
        """Fetch a single page.

        Returns:
            dict with keys:
                - "items": list of items on this page
                - "next_page": int or None
                - "total_pages": int
        """
        if self._total_pages == 0:
            return {"items": [], "next_page": None, "total_pages": 0}

        if page < 1 or page > self._total_pages:
            raise ValueError(f"Page {page} out of range (1-{self._total_pages})")

        start = (page - 1) * self._page_size
        end = start + self._page_size
        items = self._items[start:end]
        next_page = page + 1 if page < self._total_pages else None

        return {
            "items": items,
            "next_page": next_page,
            "total_pages": self._total_pages,
        }
