"""Application manager that handles database, caching, validation, and formatting."""

import re
import json
import time
import hashlib
from datetime import datetime


class AppManager:
    """Manages the entire application: database, cache, validation, and formatting."""

    def __init__(self):
        self._db_name = None
        self._connected = False
        self._tables = {}
        self._next_id = 1
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_hits = 0
        self._cache_misses = 0

    # ---- Database operations ----

    def connect(self, db_name):
        """Connect to a database."""
        if self._connected:
            self.disconnect()
        self._db_name = db_name
        self._connected = True
        self._tables = {}
        self._next_id = 1
        return {"status": "connected", "database": db_name}

    def disconnect(self):
        """Disconnect from the database."""
        if not self._connected:
            return {"status": "already disconnected"}
        db_name = self._db_name
        self._db_name = None
        self._connected = False
        return {"status": "disconnected", "database": db_name}

    def query(self, table, conditions=None):
        """Query records from a table."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        if table not in self._tables:
            return []
        records = self._tables[table]
        if conditions is None:
            return list(records)
        result = []
        for record in records:
            match = True
            for key, value in conditions.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                result.append(dict(record))
        return result

    def insert(self, table, record):
        """Insert a record into a table."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        if table not in self._tables:
            self._tables[table] = []
        new_record = dict(record)
        new_record["id"] = self._next_id
        self._next_id += 1
        self._tables[table].append(new_record)
        return {"inserted": True, "id": new_record["id"]}

    def update(self, table, record_id, fields):
        """Update a record in a table."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        if table not in self._tables:
            return {"updated": False, "error": "table not found"}
        for record in self._tables[table]:
            if record.get("id") == record_id:
                for key, value in fields.items():
                    record[key] = value
                return {"updated": True, "id": record_id}
        return {"updated": False, "error": "record not found"}

    def delete(self, table, record_id):
        """Delete a record from a table."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        if table not in self._tables:
            return {"deleted": False, "error": "table not found"}
        for i, record in enumerate(self._tables[table]):
            if record.get("id") == record_id:
                self._tables[table].pop(i)
                return {"deleted": True, "id": record_id}
        return {"deleted": False, "error": "record not found"}

    def count(self, table, conditions=None):
        """Count records in a table, optionally filtered by conditions."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        return len(self.query(table, conditions))

    def table_exists(self, table):
        """Check if a table exists in the database."""
        if not self._connected:
            raise ConnectionError("not connected to a database")
        return table in self._tables

    # ---- Cache operations ----

    def get_cache(self, key):
        """Get a value from cache."""
        if key in self._cache:
            ts = self._cache_timestamps.get(key, {})
            ttl = ts.get("ttl", float("inf"))
            created = ts.get("created", 0)
            if time.time() - created > ttl:
                del self._cache[key]
                del self._cache_timestamps[key]
                self._cache_misses += 1
                return None
            self._cache_hits += 1
            return self._cache[key]
        self._cache_misses += 1
        return None

    def set_cache(self, key, value, ttl=3600):
        """Set a value in cache with a TTL in seconds."""
        self._cache[key] = value
        self._cache_timestamps[key] = {"created": time.time(), "ttl": ttl}
        return {"cached": True, "key": key}

    def clear_cache(self):
        """Clear all cache entries."""
        count = len(self._cache)
        self._cache.clear()
        self._cache_timestamps.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        return {"cleared": True, "entries_removed": count}

    def has_cache(self, key):
        """Check if a key exists in cache (without counting as hit/miss)."""
        return key in self._cache

    def get_cache_stats(self):
        """Return cache statistics."""
        total = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total * 100) if total > 0 else 0.0
        return {
            "entries": len(self._cache),
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": round(hit_rate, 2),
        }

    # ---- Validation operations ----

    def validate_user(self, data):
        """Validate user data."""
        errors = []
        if not isinstance(data, dict):
            return {"valid": False, "errors": ["data must be a dict"]}
        if not data.get("name") or not isinstance(data["name"], str):
            errors.append("name is required and must be a string")
        if "age" not in data or not isinstance(data["age"], int) or data["age"] < 0:
            errors.append("age must be a non-negative integer")
        if "email" not in data or not self.validate_email(data.get("email", "")):
            errors.append("valid email is required")
        return {"valid": len(errors) == 0, "errors": errors}

    def validate_order(self, data):
        """Validate order data."""
        errors = []
        if not isinstance(data, dict):
            return {"valid": False, "errors": ["data must be a dict"]}
        if not data.get("product"):
            errors.append("product is required")
        if "quantity" not in data or not isinstance(data["quantity"], int) or data["quantity"] < 1:
            errors.append("quantity must be a positive integer")
        if "price" not in data or not isinstance(data["price"], (int, float)) or data["price"] <= 0:
            errors.append("price must be a positive number")
        return {"valid": len(errors) == 0, "errors": errors}

    def validate_email(self, email):
        """Validate an email address. Returns True/False."""
        if not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def validate_phone(self, phone):
        """Validate a phone number. Returns True/False."""
        if not isinstance(phone, str):
            return False
        digits = re.sub(r"[\s\-\(\)\+]", "", phone)
        return len(digits) >= 10 and len(digits) <= 15 and digits.isdigit()

    def validate_address(self, address):
        """Validate an address dict."""
        errors = []
        if not isinstance(address, dict):
            return {"valid": False, "errors": ["address must be a dict"]}
        for field in ("street", "city", "state", "zip_code"):
            if not address.get(field):
                errors.append(f"{field} is required")
        if address.get("zip_code") and not re.match(r"^\d{5}(-\d{4})?$", str(address["zip_code"])):
            errors.append("zip_code must be in format XXXXX or XXXXX-XXXX")
        return {"valid": len(errors) == 0, "errors": errors}

    def validate_record(self, data, required_fields):
        """Generic record validation — checks that all required fields are present and non-empty."""
        errors = []
        if not isinstance(data, dict):
            return {"valid": False, "errors": ["data must be a dict"]}
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
        return {"valid": len(errors) == 0, "errors": errors}

    # ---- Formatting operations ----

    def format_report(self, title, data):
        """Format data into a report string."""
        lines = []
        lines.append("=" * 50)
        lines.append(title.upper().center(50))
        lines.append("=" * 50)
        lines.append("")
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    lines.append(f"  Record {i}:")
                    for key, value in item.items():
                        lines.append(f"    {key}: {value}")
                else:
                    lines.append(f"  {i}. {item}")
                lines.append("")
        elif isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        lines.append("=" * 50)
        return "\n".join(lines)

    def format_email(self, to, subject, body):
        """Format an email message."""
        return {
            "to": to,
            "subject": subject,
            "body": body,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8",
                "X-Mailer": "AppManager/1.0",
            },
            "formatted": f"To: {to}\nSubject: {subject}\n\n{body}",
        }

    def format_csv(self, headers, rows):
        """Format data as a CSV string."""
        lines = [",".join(str(h) for h in headers)]
        for row in rows:
            cells = []
            for cell in row:
                s = str(cell)
                if "," in s or '"' in s or "\n" in s:
                    s = '"' + s.replace('"', '""') + '"'
                cells.append(s)
            lines.append(",".join(cells))
        return "\n".join(lines)

    def format_json_response(self, data, status="success"):
        """Format a JSON API response."""
        response = {
            "status": status,
            "data": data,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        if status != "success":
            response["error"] = True
        return response

    def format_log_entry(self, level, message):
        """Format a log entry string."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        level_upper = level.upper()
        return f"[{timestamp}] [{level_upper}] {message}"

    def format_table(self, headers, rows):
        """Format data as a plain-text table with aligned columns."""
        all_rows = [headers] + rows
        col_widths = []
        for col in range(len(headers)):
            max_w = 0
            for row in all_rows:
                if col < len(row):
                    max_w = max(max_w, len(str(row[col])))
            col_widths.append(max_w)
        lines = []
        for row in all_rows:
            cells = []
            for col, cell in enumerate(row):
                cells.append(str(cell).ljust(col_widths[col]))
            lines.append("  ".join(cells))
            if row is headers:
                lines.append("  ".join("-" * w for w in col_widths))
        return "\n".join(lines)
