# Challenge 112: Cascading Failures

The three modules in `setup/` have bugs. Fix them so all tests pass.

**Warning:** the modules are interdependent -- changing one may affect others. The bugs form a chain: fixing one module may reveal or create issues in the next.

- `setup/parser.py` - Parses CSV text into records
- `setup/formatter.py` - Formats records into a text table
- `setup/reporter.py` - Uses parser and formatter to generate reports
