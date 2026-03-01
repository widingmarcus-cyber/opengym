# Step 1: Migrate Data to New Schema

The file `setup/data.json` contains records in an old schema:

```json
[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
```

Migrate every record to the new schema with these rules:

1. **Rename** the `name` field to `full_name` (keep the same value).
2. **Keep** the `age` field unchanged.
3. **Add** a new field `active` with a default value of `true`.
4. **Remove** the old `name` field entirely from each record.

Write the migrated data back to `setup/data.json`. After migration, the file should contain:

```json
[{"full_name": "Alice", "age": 30, "active": true}, {"full_name": "Bob", "age": 25, "active": true}]
```

The file `setup/data.json` will persist to the next session.
