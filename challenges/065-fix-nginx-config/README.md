# Challenge 065: Fix Nginx Config

## Difficulty: Medium

## Task

The file `setup/nginx.conf` has several configuration issues. Fix all the problems so that the Nginx configuration correctly serves a web application with an API proxy, SSL redirect, and gzip compression.

## Setup

- `setup/nginx.conf` — A broken Nginx configuration file

## Requirements

Fix the Nginx configuration so that:

1. HTTP (port 80) requests are redirected to HTTPS (port 443)
2. The main server block listens on port 443 with SSL
3. The `location /api/` block proxies to the backend at `http://localhost:8000` with a trailing slash on the proxy_pass URL
4. Static files are served from `/var/www/html`
5. Gzip compression is enabled with appropriate settings
6. Proxy headers (`X-Real-IP`, `X-Forwarded-For`, `Host`) are set in the API location block

## Rules

- Only modify `setup/nginx.conf`
- The resulting file must be syntactically valid Nginx configuration
