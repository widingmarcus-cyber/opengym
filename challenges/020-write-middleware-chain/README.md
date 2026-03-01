# Challenge 020: Write Middleware Chain

## Difficulty: Medium

## Task

The file `setup/middleware.py` is empty. Implement a middleware pipeline system with `Request` and `Response` dataclasses and a `Pipeline` class.

## Requirements

### Dataclasses

- `Request` — A dataclass with a `data` field (dict, default empty dict)
- `Response` — A dataclass with a `data` field (dict, default empty dict)

### Pipeline class

1. `use(middleware_fn)` — Register a middleware function. Returns `self` for chaining
2. `execute(request)` — Run the request through all registered middleware in order, returning the final `Response`

### Middleware functions

Each middleware function has the signature `middleware(request, next_fn)` where:
- `request` is a `Request` object
- `next_fn` is a callable that takes a `Request` and returns a `Response`
- The middleware can modify the request before calling `next_fn`, and modify the response after

If no middleware is registered, `execute` should return `Response()`.

## Rules

- Only modify files in the `setup/` directory
- Middleware must execute in the order they are registered
- Each middleware must be able to short-circuit (not call `next_fn`) and return its own `Response`

## Examples

```python
def logging_middleware(request, next_fn):
    request.data["logged"] = True
    response = next_fn(request)
    return response

def auth_middleware(request, next_fn):
    if not request.data.get("token"):
        return Response(data={"error": "unauthorized"})
    return next_fn(request)

pipeline = Pipeline()
pipeline.use(logging_middleware).use(auth_middleware)

req = Request(data={"token": "abc123"})
resp = pipeline.execute(req)
```
