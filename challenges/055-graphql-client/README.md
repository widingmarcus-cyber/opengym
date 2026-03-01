# Challenge 055: GraphQL Client

## Difficulty: Hard

## Task

Build a GraphQL query builder and client. Implement the classes in `setup/graphql_client.py`.

## Setup

`setup/graphql_server.py` provides a simulated `GraphQLServer` class:
- `execute(query_str, variables=None)` — Executes a GraphQL query string and returns a dict with `"data"` key on success, or `"errors"` key on failure

## Requirements

Implement in `setup/graphql_client.py`:

### `QueryBuilder` class

A fluent query builder:

1. `select(*fields)` — Add fields to select. Returns `self` for chaining.
2. `where(**filters)` — Add filter arguments. Returns `self` for chaining.
3. `nested(field, sub_builder)` — Add a nested selection on a field using another `QueryBuilder`. Returns `self` for chaining.
4. `build()` — Return the built GraphQL query string.

Example: `QueryBuilder("users").select("id", "name").where(active=True).build()` produces:
`{ users(active: true) { id name } }`

### `GraphQLClient` class

1. Constructor: `GraphQLClient(server)` — Wraps the GraphQL server.
2. `query(query_str, variables=None)` — Execute a raw query string. Returns the `"data"` dict on success. Raises `RuntimeError` with the error messages if the response contains `"errors"`.
3. `execute_builder(builder)` — Build the query from a `QueryBuilder` and execute it. Returns the `"data"` dict or raises `RuntimeError`.

## Rules

- Only modify files in the `setup/` directory (do not modify `graphql_server.py`)
- Boolean values in `where()` should render as `true`/`false` (GraphQL convention)
- String values in `where()` should be quoted with double quotes
- Integer values render as-is
