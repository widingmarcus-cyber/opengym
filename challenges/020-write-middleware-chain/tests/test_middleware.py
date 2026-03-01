"""Tests for Challenge 020: Write Middleware Chain."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from middleware import Pipeline, Request, Response


def test_empty_pipeline():
    pipeline = Pipeline()
    req = Request(data={"key": "value"})
    resp = pipeline.execute(req)
    assert isinstance(resp, Response)


def test_single_middleware():
    def add_header(request, next_fn):
        request.data["processed"] = True
        return next_fn(request)

    pipeline = Pipeline()
    pipeline.use(add_header)
    req = Request(data={})
    resp = pipeline.execute(req)
    assert isinstance(resp, Response)


def test_middleware_modifies_request():
    def enrich(request, next_fn):
        request.data["enriched"] = True
        response = next_fn(request)
        response.data["request_was_enriched"] = request.data.get("enriched", False)
        return response

    pipeline = Pipeline()
    pipeline.use(enrich)
    req = Request(data={})
    resp = pipeline.execute(req)
    assert resp.data.get("request_was_enriched") is True


def test_middleware_order():
    call_order = []

    def first(request, next_fn):
        call_order.append("first")
        return next_fn(request)

    def second(request, next_fn):
        call_order.append("second")
        return next_fn(request)

    pipeline = Pipeline()
    pipeline.use(first)
    pipeline.use(second)
    pipeline.execute(Request())
    assert call_order == ["first", "second"]


def test_middleware_short_circuit():
    def blocker(request, next_fn):
        return Response(data={"blocked": True})

    def unreachable(request, next_fn):
        return Response(data={"reached": True})

    pipeline = Pipeline()
    pipeline.use(blocker)
    pipeline.use(unreachable)
    resp = pipeline.execute(Request())
    assert resp.data.get("blocked") is True
    assert resp.data.get("reached") is None


def test_middleware_modifies_response():
    def add_timestamp(request, next_fn):
        response = next_fn(request)
        response.data["timestamp"] = "2024-01-01"
        return response

    pipeline = Pipeline()
    pipeline.use(add_timestamp)
    resp = pipeline.execute(Request())
    assert resp.data["timestamp"] == "2024-01-01"


def test_chaining_use():
    def m1(request, next_fn):
        return next_fn(request)

    def m2(request, next_fn):
        return next_fn(request)

    pipeline = Pipeline()
    result = pipeline.use(m1).use(m2)
    assert result is pipeline


def test_auth_pattern():
    def auth(request, next_fn):
        if not request.data.get("token"):
            return Response(data={"error": "unauthorized"})
        return next_fn(request)

    def handler(request, next_fn):
        response = next_fn(request)
        response.data["result"] = "success"
        return response

    pipeline = Pipeline()
    pipeline.use(auth).use(handler)

    resp_no_auth = pipeline.execute(Request(data={}))
    assert resp_no_auth.data.get("error") == "unauthorized"

    resp_auth = pipeline.execute(Request(data={"token": "valid"}))
    assert resp_auth.data.get("result") == "success"
