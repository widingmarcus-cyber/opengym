"""Product search module for an e-commerce catalog."""


def build_index(products):
    """Build a search index from a list of product dicts.

    Each product dict has keys: 'id', 'name', 'category'.
    Returns an index object to be passed to search().
    """
    return {"products": products}


def _find_in_list(products, query):
    """Search for products matching the query by scanning the list."""
    results = []
    query_lower = query.lower()
    for product in products:
        name_lower = product["name"].lower()
        if query_lower in name_lower:
            results.append(product)
    return results


def search(index, query):
    """Search for products whose name contains the query string.

    Args:
        index: The search index built by build_index()
        query: Search string (case-insensitive partial match)

    Returns:
        List of product dicts matching the query
    """
    return _find_in_list(index["products"], query)


def search_by_category(index, category):
    """Return all products in a given category.

    Args:
        index: The search index built by build_index()
        category: Category string (case-insensitive exact match)

    Returns:
        List of product dicts in the category
    """
    results = []
    cat_lower = category.lower()
    for product in index["products"]:
        if product["category"].lower() == cat_lower:
            results.append(product)
    return results
