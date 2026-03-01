# Challenge 237: Dependency Resolution

## Objective

Resolve a complex dependency graph with version constraints and conflicts. Given a set of packages with version requirements, find a valid resolution that satisfies all constraints, or report that resolution is impossible.

## Setup

- `setup/packages.json` - A registry of available packages and their versions, each with their own dependencies.
- `setup/requirements.json` - The top-level requirements to resolve (package names with version constraints).

## Task

1. Read `setup/requirements.json` for the top-level packages needed.
2. Read `setup/packages.json` for all available packages and their versions/dependencies.
3. Resolve the full dependency tree:
   - Each requirement specifies a package and a version constraint (e.g., `>=1.0.0,<2.0.0`).
   - Each package version may have its own dependencies with version constraints.
   - Find a set of package versions that satisfies ALL constraints simultaneously.
4. Write `setup/resolution.json` with the resolved dependency tree.
5. Write `setup/install_order.json` with the topologically sorted installation order.

## Version Constraint Syntax

- `>=1.0.0` - greater than or equal to 1.0.0
- `<2.0.0` - less than 2.0.0
- `>=1.0.0,<2.0.0` - combined constraints (AND)
- `==1.5.0` - exact version

## Output Format

`setup/resolution.json`:
```json
{
  "resolved": true,
  "packages": {
    "<package_name>": {
      "version": "<selected_version>",
      "dependencies": ["<dep_name>@<dep_version>", ...]
    },
    ...
  },
  "total_packages": <number>
}
```

`setup/install_order.json`:
```json
{
  "order": ["<package_name>@<version>", ...],
  "total_steps": <number>
}
```

## Constraints

- If a package has no version that satisfies all constraints, report `"resolved": false` with a `"conflict"` field explaining the issue.
- The install order must be topologically sorted: a package is installed only after all its dependencies are installed.
- Choose the highest compatible version when multiple versions satisfy a constraint.
