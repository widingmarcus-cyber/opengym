"""Tests for Challenge 055: GraphQL Client."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from graphql_server import GraphQLServer
from graphql_client import QueryBuilder, GraphQLClient


def test_query_builder_simple():
    builder = QueryBuilder("users").select("id", "name")
    query = builder.build()
    assert "users" in query
    assert "id" in query
    assert "name" in query


def test_query_builder_with_filters():
    builder = QueryBuilder("users").select("id", "name").where(active=True)
    query = builder.build()
    assert "active: true" in query


def test_query_builder_string_filter():
    builder = QueryBuilder("users").select("id").where(role="admin")
    query = builder.build()
    assert 'role: "admin"' in query


def test_query_builder_integer_filter():
    builder = QueryBuilder("users").select("id").where(age=25)
    query = builder.build()
    assert "age: 25" in query


def test_query_builder_nested():
    posts_builder = QueryBuilder("posts").select("title", "body")
    builder = QueryBuilder("users").select("id", "name").nested("posts", posts_builder)
    query = builder.build()
    assert "posts" in query
    assert "title" in query
    assert "body" in query


def test_client_query_success():
    server = GraphQLServer(data={"users": [{"id": 1, "name": "Alice"}]})
    client = GraphQLClient(server)
    result = client.query("{ users { id name } }")
    assert result == {"users": [{"id": 1, "name": "Alice"}]}


def test_client_query_error():
    server = GraphQLServer(data={})
    client = GraphQLClient(server)
    with pytest.raises(RuntimeError, match="Unknown field"):
        client.query("{ nonexistent { id } }")


def test_client_execute_builder():
    server = GraphQLServer(data={"users": [{"id": 1}]})
    client = GraphQLClient(server)
    builder = QueryBuilder("users").select("id")
    result = client.execute_builder(builder)
    assert result == {"users": [{"id": 1}]}


def test_client_empty_query_error():
    server = GraphQLServer(data={})
    client = GraphQLClient(server)
    with pytest.raises(RuntimeError, match="Empty query"):
        client.query("")


def test_query_builder_chaining():
    builder = QueryBuilder("products")
    result = builder.select("id", "name").where(category="electronics").select("price")
    assert result is builder
    query = builder.build()
    assert "id" in query
    assert "name" in query
    assert "price" in query
    assert 'category: "electronics"' in query
