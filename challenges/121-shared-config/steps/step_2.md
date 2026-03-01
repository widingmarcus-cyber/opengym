You are Agent B. Write the CACHE section of setup/shared_config.yaml:

```yaml
cache:
  provider: redis
  host: cache.internal.company.com
  port: 6379
  ttl: 3600
  max_memory: 512mb
```

IMPORTANT: If setup/shared_config.yaml already has other sections (like database), you MUST preserve them. Only add/update the cache section.
