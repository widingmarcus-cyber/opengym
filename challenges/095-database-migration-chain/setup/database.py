class InMemoryDB:
    def __init__(self):
        self._tables = {}
        self._schemas = {}

    def create_table(self, name, columns):
        if name in self._tables:
            raise ValueError(f"Table '{name}' already exists")
        self._schemas[name] = dict(columns)
        self._tables[name] = []

    def add_column(self, table, col_name, col_type, default=None):
        if table not in self._schemas:
            raise ValueError(f"Table '{table}' does not exist")
        if col_name in self._schemas[table]:
            raise ValueError(f"Column '{col_name}' already exists in '{table}'")
        self._schemas[table][col_name] = col_type
        for row in self._tables[table]:
            row[col_name] = default

    def rename_column(self, table, old_name, new_name):
        if table not in self._schemas:
            raise ValueError(f"Table '{table}' does not exist")
        if old_name not in self._schemas[table]:
            raise ValueError(f"Column '{old_name}' does not exist in '{table}'")
        col_type = self._schemas[table].pop(old_name)
        self._schemas[table][new_name] = col_type
        for row in self._tables[table]:
            row[new_name] = row.pop(old_name)

    def drop_column(self, table, col_name):
        if table not in self._schemas:
            raise ValueError(f"Table '{table}' does not exist")
        if col_name not in self._schemas[table]:
            raise ValueError(f"Column '{col_name}' does not exist in '{table}'")
        del self._schemas[table][col_name]
        for row in self._tables[table]:
            row.pop(col_name, None)

    def insert(self, table, row):
        if table not in self._tables:
            raise ValueError(f"Table '{table}' does not exist")
        full_row = {}
        for col in self._schemas[table]:
            full_row[col] = row.get(col)
        self._tables[table].append(full_row)

    def query(self, table, filter_fn=None):
        if table not in self._tables:
            raise ValueError(f"Table '{table}' does not exist")
        rows = self._tables[table]
        if filter_fn:
            rows = [r for r in rows if filter_fn(r)]
        return [dict(r) for r in rows]

    def get_schema(self, table):
        if table not in self._schemas:
            raise ValueError(f"Table '{table}' does not exist")
        return dict(self._schemas[table])

    def list_tables(self):
        return list(self._tables.keys())
