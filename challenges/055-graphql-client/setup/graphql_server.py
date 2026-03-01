import re


class GraphQLServer:
    """Simulated GraphQL server."""

    def __init__(self, data=None):
        self._data = data or {}

    def execute(self, query_str, variables=None):
        """Execute a GraphQL query string.

        Returns a dict with "data" on success or "errors" on failure.
        """
        query_str = query_str.strip()
        if not query_str:
            return {"errors": [{"message": "Empty query"}]}

        root_match = re.match(r"\{\s*(\w+)", query_str)
        if not root_match:
            return {"errors": [{"message": "Invalid query syntax"}]}

        root_field = root_match.group(1)

        if root_field not in self._data:
            return {"errors": [{"message": f"Unknown field: {root_field}"}]}

        result = self._data[root_field]

        if callable(result):
            try:
                result = result(query_str, variables)
            except Exception as e:
                return {"errors": [{"message": str(e)}]}

        return {"data": {root_field: result}}
