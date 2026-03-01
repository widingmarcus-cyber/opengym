# WidgetAPI Documentation v3.2.1

## Overview

WidgetAPI is a RESTful service for managing widget inventories. It was originally developed in 2019 by the Acme Corporation engineering team. The API follows OpenAPI 3.0 specification and uses JSON for all request and response bodies.

## Authentication

All API requests require authentication via Bearer tokens. Tokens are obtained from the `/auth/token` endpoint using your API key and secret.

**Token Lifetime:** Access tokens expire after 3600 seconds (1 hour). Refresh tokens expire after 30 days.

**Rate Limiting:** The API enforces a rate limit of 500 requests per minute per API key. When exceeded, the API returns HTTP 429 with a `Retry-After` header.

### Obtaining a Token

```
POST /auth/token
Content-Type: application/json

{
    "api_key": "your-key",
    "api_secret": "your-secret"
}
```

Response:
```json
{
    "access_token": "eyJhbG...",
    "refresh_token": "dGhpcyB...",
    "expires_in": 3600,
    "token_type": "Bearer"
}
```

## Widgets

### Widget Object

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier |
| name | string | Widget name (max 128 characters) |
| category | string | One of: "standard", "premium", "enterprise" |
| weight_grams | integer | Weight in grams |
| price_cents | integer | Price in cents (USD) |
| created_at | string (ISO 8601) | Creation timestamp |
| metadata | object | Arbitrary key-value pairs (max 10 keys) |

### List Widgets

```
GET /api/v2/widgets
```

Query parameters:
- `page` (integer, default: 1) — Page number
- `per_page` (integer, default: 25, max: 100) — Items per page
- `category` (string) — Filter by category
- `sort` (string, default: "created_at") — Sort field
- `order` (string, default: "desc") — Sort order: "asc" or "desc"

### Create Widget

```
POST /api/v2/widgets
Content-Type: application/json

{
    "name": "My Widget",
    "category": "standard",
    "weight_grams": 150,
    "price_cents": 1999,
    "metadata": {"color": "blue"}
}
```

**Required fields:** name, category, weight_grams, price_cents

**Validation Rules:**
- `name` must be 1-128 characters, alphanumeric and spaces only
- `category` must be one of the allowed values
- `weight_grams` must be a positive integer, max 50000
- `price_cents` must be a non-negative integer

### Update Widget

```
PATCH /api/v2/widgets/{id}
```

Supports partial updates. Only send the fields you want to change.

### Delete Widget

```
DELETE /api/v2/widgets/{id}
```

Returns HTTP 204 on success. Deletion is **soft** — widgets are marked as deleted and excluded from list results, but can be restored within 90 days via `POST /api/v2/widgets/{id}/restore`.

## Bulk Operations

### Bulk Import

```
POST /api/v2/widgets/bulk
Content-Type: application/json

{
    "widgets": [...],
    "on_conflict": "skip"  // or "update" or "error"
}
```

**Maximum batch size:** 1000 widgets per request.

The `on_conflict` parameter controls behavior when a widget with the same name already exists:
- `skip` — Silently skip duplicates
- `update` — Update existing widget with new data
- `error` — Return an error for the entire batch

## Webhooks

WidgetAPI supports webhooks for real-time event notifications.

### Supported Events

| Event | Description |
|-------|-------------|
| widget.created | Fired when a new widget is created |
| widget.updated | Fired when a widget is modified |
| widget.deleted | Fired when a widget is deleted |
| inventory.low | Fired when stock drops below threshold |
| bulk.completed | Fired when a bulk operation finishes |

### Webhook Payload

```json
{
    "event": "widget.created",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": { ... },
    "signature": "sha256=abc123..."
}
```

Webhook payloads are signed using HMAC-SHA256 with your webhook secret. Always verify the signature before processing.

### Retry Policy

Failed webhook deliveries are retried with exponential backoff: 1 minute, 5 minutes, 30 minutes, 2 hours, 24 hours. After 5 failed attempts, the webhook is disabled and an email notification is sent.

## Error Handling

All errors follow this format:

```json
{
    "error": {
        "code": "WIDGET_NOT_FOUND",
        "message": "The requested widget does not exist.",
        "request_id": "req_abc123"
    }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_TOKEN | 401 | Token is missing or invalid |
| TOKEN_EXPIRED | 401 | Access token has expired |
| RATE_LIMITED | 429 | Too many requests |
| WIDGET_NOT_FOUND | 404 | Widget does not exist |
| VALIDATION_ERROR | 422 | Request body failed validation |
| CONFLICT | 409 | Widget with this name already exists |
| BULK_TOO_LARGE | 413 | Bulk request exceeds 1000 items |
| INTERNAL_ERROR | 500 | Unexpected server error |

## SDKs

Official SDKs are available for:
- Python: `pip install widgetapi` (v2.1.0)
- JavaScript: `npm install @widgetapi/sdk` (v3.0.2)
- Go: `go get github.com/widgetapi/go-sdk` (v1.4.0)
- Ruby: `gem install widgetapi` (v1.2.3)

## Changelog

### v3.2.1 (2024-12-01)
- Fixed webhook retry timing for `inventory.low` events
- Added `metadata` field to widget objects

### v3.2.0 (2024-09-15)
- Added bulk import endpoint
- Introduced `on_conflict` parameter for bulk operations
- Increased rate limit from 200 to 500 requests per minute

### v3.1.0 (2024-06-01)
- Added webhook support
- Added soft delete with 90-day restoration window

### v3.0.0 (2024-01-15)
- Breaking: API path changed from `/api/v1/` to `/api/v2/`
- Breaking: Widget `price` field renamed to `price_cents` (now integer)
- Added `enterprise` category
