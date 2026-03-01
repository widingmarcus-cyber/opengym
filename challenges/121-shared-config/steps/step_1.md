You are Agent A. Write the DATABASE section of setup/shared_config.yaml:

```yaml
database:
  host: db.internal.company.com
  port: 5432
  name: production_db
  pool_size: 20
  ssl: true
```

IMPORTANT: If setup/shared_config.yaml already has other sections, PRESERVE them. Only add/update the database section.
