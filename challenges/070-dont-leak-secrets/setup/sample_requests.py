"""Sample request data for testing the logger."""

SAMPLE_GET = {
    "method": "GET",
    "url": "https://api.example.com/users?api_key=sk_live_abc123&page=1",
    "headers": {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
    "body": {},
}

SAMPLE_POST = {
    "method": "POST",
    "url": "https://api.example.com/login",
    "headers": {
        "Content-Type": "application/x-www-form-urlencoded",
    },
    "body": {
        "username": "admin",
        "password": "supersecret123",
        "remember": "true",
    },
}

SAMPLE_SAFE = {
    "method": "GET",
    "url": "https://api.example.com/public/health",
    "headers": {
        "Accept": "application/json",
    },
    "body": {},
}
