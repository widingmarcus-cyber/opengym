# Changelog

All notable changes to this project will be documented in this file.

## [2.5.0] - 2024-11-01

### New Features
- Added WebSocket support for real-time notifications
- Introduced batch processing API endpoint
- Added CSV export functionality for reports

### Bug Fixes
- Fixed memory leak in connection pooling
- Resolved race condition in cache invalidation

## [2.4.1] - 2024-09-15

### Bug Fixes
- Fixed authentication token refresh failing silently
- Patched XSS vulnerability in user input fields
- Fixed pagination offset calculation for large datasets

## [2.4.0] - 2024-08-01

### New Features
- Added role-based access control (RBAC)
- Introduced API rate limiting per user tier
- Added support for custom webhook headers

### Breaking Changes
- Removed deprecated `/api/v1/auth` endpoint
- Changed rate limit response code from 429 to 503 for enterprise tier

### Bug Fixes
- Fixed timezone handling in scheduled tasks

## [2.3.0] - 2024-06-15

### New Features
- Added full-text search across all resources
- Introduced audit logging for admin actions

### Bug Fixes
- Fixed file upload size validation bypass
- Resolved deadlock in concurrent batch operations

## [2.2.1] - 2024-05-01

### Bug Fixes
- Fixed regression in OAuth2 callback handling
- Patched SQL injection vulnerability in search endpoint

## [2.2.0] - 2024-03-20

### New Features
- Added GraphQL API alongside REST
- Introduced data export scheduling
- Added multi-language support for error messages

### Breaking Changes
- Renamed `api_key` field to `access_token` in all responses
- Removed support for TLS 1.0 and 1.1

### Bug Fixes
- Fixed incorrect pagination headers

## [2.1.0] - 2024-01-10

### New Features
- Added two-factor authentication support
- Introduced request/response compression

### Bug Fixes
- Fixed session timeout not being respected
- Resolved memory spike during large file uploads

## [2.0.0] - 2023-11-01

### New Features
- Complete API redesign with versioned endpoints
- Added OpenAPI 3.0 specification
- Introduced async job processing

### Breaking Changes
- Migrated from REST v1 to v2 API format
- Changed authentication from API keys to OAuth2
- Removed XML response format support

### Bug Fixes
- Fixed data corruption in concurrent writes

## [1.9.0] - 2023-09-01

### New Features
- Added webhook retry mechanism with exponential backoff
- Introduced request tracing with correlation IDs

### Bug Fixes
- Fixed incorrect HTTP status codes for validation errors
- Resolved timeout issues with large payload processing

## [1.8.1] - 2023-07-15

### Bug Fixes
- Fixed critical security vulnerability in JWT validation
- Patched denial of service vector in file parsing
- Fixed incorrect error messages for 404 responses

## [1.8.0] - 2023-06-01

### New Features
- Added IP allowlisting for API access
- Introduced custom field mapping for data imports

### Bug Fixes
- Fixed race condition in distributed lock mechanism

## [1.7.0] - 2023-04-15

### New Features
- Added support for bulk delete operations
- Introduced configurable retry policies

### Breaking Changes
- Changed default pagination size from 100 to 50

### Bug Fixes
- Fixed memory leak in event stream handler
- Resolved incorrect sorting for nested fields

## [1.6.0] - 2023-02-01

### New Features
- Added real-time event streaming via SSE
- Introduced API usage analytics dashboard

### Bug Fixes
- Fixed token expiration check off-by-one error

## [1.5.1] - 2023-01-01

### Bug Fixes
- Fixed critical data loss bug in batch update endpoint
- Patched authentication bypass in admin panel
- Resolved intermittent 500 errors on health check endpoint

## [1.5.0] - 2022-11-15

### New Features
- Added support for custom data transformations
- Introduced automated backup scheduling

### Breaking Changes
- Replaced `callback_url` with `webhook_url` in all configurations

### Bug Fixes
- Fixed incorrect timestamp formatting in logs

## [1.4.0] - 2022-09-01

### New Features
- Added multi-tenant support
- Introduced field-level encryption for sensitive data

### Bug Fixes
- Fixed permission escalation vulnerability
- Resolved connection timeout in clustered deployment

## [1.3.0] - 2022-07-01

### New Features
- Added CSV import functionality
- Introduced API versioning headers

### Bug Fixes
- Fixed incorrect content-type negotiation

## [1.2.0] - 2022-04-15

### New Features
- Added email notification integration
- Introduced request caching layer

### Breaking Changes
- Changed date format from Unix timestamp to ISO 8601

### Bug Fixes
- Fixed broken pagination in search results
- Resolved memory issues with large response payloads

## [1.1.0] - 2022-03-01

### New Features
- Added filtering and sorting for list endpoints
- Introduced health check endpoint

### Bug Fixes
- Fixed incorrect HTTP method routing
- Resolved encoding issues with Unicode characters

## [1.0.0] - 2022-01-15

### New Features
- Initial public release
- RESTful API with CRUD operations
- Token-based authentication
- Basic rate limiting
- JSON request/response format
