# Deployment Guide

## Environment Variables

The application is configured via the following environment variables:

### Application Settings
| Variable         | Description                      | Default     |
|-----------------|----------------------------------|-------------|
| APP_PORT        | Port the application listens on  | 8080        |
| APP_ENV         | Environment (development/production) | development |
| APP_SECRET_KEY  | Secret key for JWT signing       | (required)  |
| APP_LOG_LEVEL   | Logging level                    | info        |

### Database Settings
| Variable         | Description                      | Default     |
|-----------------|----------------------------------|-------------|
| DB_HOST         | Database server hostname         | localhost   |
| DB_PORT         | Database server port             | 5432        |
| DB_NAME         | Database name                    | appdb       |
| DB_USER         | Database username                | postgres    |
| DB_PASSWORD     | Database password                | (required)  |
| DB_MAX_CONNECTIONS | Maximum connection pool size  | 20          |

### Cache Settings
| Variable         | Description                      | Default     |
|-----------------|----------------------------------|-------------|
| CACHE_ENABLED   | Enable response caching          | true        |
| CACHE_HOST      | Redis host for caching           | localhost   |
| CACHE_PORT      | Redis port                       | 6379        |

## Deployment Profiles

### Development
- APP_PORT: 3000
- APP_ENV: development
- DB_HOST: localhost
- Debug mode enabled

### Staging
- APP_PORT: 8080
- APP_ENV: staging
- DB_HOST: staging-db.internal
- SSL required

### Production
- APP_PORT: 443
- APP_ENV: production
- DB_HOST: prod-db-cluster.internal
- SSL required
- DB_MAX_CONNECTIONS: 100
- Minimum 3 replicas recommended

## Health Checks

The `/api/health` endpoint should return HTTP 200 with `{"status": "ok"}`. Configure your load balancer to poll this endpoint every 30 seconds.
