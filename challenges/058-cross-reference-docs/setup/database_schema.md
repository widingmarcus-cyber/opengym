# Database Schema

## Connection

The application connects to a PostgreSQL database. Connection parameters are configured via environment variables.

## Tables

### users
| Column     | Type         | Constraints          |
|------------|-------------|----------------------|
| id         | SERIAL      | PRIMARY KEY          |
| name       | VARCHAR(100) | NOT NULL            |
| email      | VARCHAR(255) | NOT NULL, UNIQUE    |
| password_hash | VARCHAR(255) | NOT NULL         |
| role       | VARCHAR(20)  | DEFAULT 'user'      |
| created_at | TIMESTAMP    | DEFAULT NOW()       |

### sessions
| Column     | Type         | Constraints          |
|------------|-------------|----------------------|
| id         | SERIAL      | PRIMARY KEY          |
| user_id    | INTEGER     | REFERENCES users(id) |
| token      | VARCHAR(500) | NOT NULL, UNIQUE    |
| expires_at | TIMESTAMP    | NOT NULL            |
| created_at | TIMESTAMP    | DEFAULT NOW()       |

### products
| Column     | Type         | Constraints          |
|------------|-------------|----------------------|
| id         | SERIAL      | PRIMARY KEY          |
| name       | VARCHAR(200) | NOT NULL            |
| description | TEXT        |                      |
| price      | DECIMAL(10,2) | NOT NULL           |
| category   | VARCHAR(50)  |                      |
| stock      | INTEGER      | DEFAULT 0           |

### orders
| Column     | Type         | Constraints          |
|------------|-------------|----------------------|
| id         | SERIAL      | PRIMARY KEY          |
| user_id    | INTEGER     | REFERENCES users(id) |
| status     | VARCHAR(20)  | DEFAULT 'pending'   |
| total      | DECIMAL(10,2) |                     |
| created_at | TIMESTAMP    | DEFAULT NOW()       |

### order_items
| Column     | Type         | Constraints              |
|------------|-------------|--------------------------|
| id         | SERIAL      | PRIMARY KEY              |
| order_id   | INTEGER     | REFERENCES orders(id)    |
| product_id | INTEGER     | REFERENCES products(id)  |
| quantity   | INTEGER      | NOT NULL                |
| unit_price | DECIMAL(10,2) | NOT NULL               |

### audit_logs
| Column     | Type         | Constraints          |
|------------|-------------|----------------------|
| id         | SERIAL      | PRIMARY KEY          |
| user_id    | INTEGER     | REFERENCES users(id) |
| action     | VARCHAR(50)  | NOT NULL            |
| resource   | VARCHAR(100) | NOT NULL            |
| details    | JSONB        |                      |
| created_at | TIMESTAMP    | DEFAULT NOW()       |

## Indexes

- `idx_users_email` on `users(email)`
- `idx_sessions_token` on `sessions(token)`
- `idx_orders_user_id` on `orders(user_id)`
- `idx_audit_logs_user_action` on `audit_logs(user_id, action)`
