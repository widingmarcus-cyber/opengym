# API Specification

## Authentication

All endpoints under `/api/` require a valid Bearer token in the Authorization header, except for `POST /api/auth/login` and `GET /api/health`.

## Endpoints

### POST /api/auth/login
- **Description**: Authenticate a user and receive an access token
- **Auth Required**: No
- **Request Body**: `{ "email": str, "password": str }`
- **Response**: `{ "token": str, "expires_in": int }`
- **Database Operations**: Reads from `users` table, writes to `sessions` table

### GET /api/users
- **Description**: List all users (admin only)
- **Auth Required**: Yes
- **Query Parameters**: `page`, `per_page`, `sort_by`
- **Response**: `{ "users": [...], "total": int }`
- **Database Operations**: Reads from `users` table

### POST /api/users
- **Description**: Create a new user account
- **Auth Required**: Yes
- **Request Body**: `{ "name": str, "email": str, "role": str }`
- **Response**: `{ "user": {...}, "created": true }`
- **Database Operations**: Writes to `users` table, writes to `audit_logs` table

### GET /api/products
- **Description**: List available products
- **Auth Required**: Yes
- **Query Parameters**: `category`, `min_price`, `max_price`
- **Response**: `{ "products": [...] }`
- **Database Operations**: Reads from `products` table
- **Caching**: Results cached with TTL of 300 seconds

### POST /api/orders
- **Description**: Place a new order
- **Auth Required**: Yes
- **Request Body**: `{ "items": [{"product_id": int, "quantity": int}] }`
- **Response**: `{ "order": {...} }`
- **Database Operations**: Reads from `products` table, writes to `orders` table, writes to `order_items` table, writes to `audit_logs` table

### GET /api/orders
- **Description**: List orders for the authenticated user
- **Auth Required**: Yes
- **Query Parameters**: `status`, `from_date`, `to_date`
- **Response**: `{ "orders": [...] }`
- **Database Operations**: Reads from `orders` table, reads from `order_items` table

### GET /api/health
- **Description**: Health check endpoint
- **Auth Required**: No
- **Response**: `{ "status": "ok", "version": str }`
- **Database Operations**: None
