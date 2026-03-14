# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 123 new challenges (total: 250) across 8 new categories:
  - Memory & State (128-147): append-only logs, state merge, schema migration, LRU eviction, WAL
  - Concurrency & Coordination (148-165): file locking, atomic counters, producer-consumer, leader election
  - Tool Robustness (166-185): retry-after, malformed JSON, paginated APIs, deprecated migration
  - Scheduling & Cron (186-197): cron policies, missed schedules, timezone/DST, idempotency
  - Failure Recovery (198-212): crash recovery, OOM, disk full, SIGTERM, atomicity, rollback
  - Security & Boundary (213-222): path traversal, secret leaks, injection, deserialization, rate limiting
  - Observability & Determinism (223-232): log parsing, metrics, tracing, dedup, reproducible builds
  - Long-Horizon Stability (233-250): 10-stage pipeline, config drift, state machines, consensus
- `docs/ARCHITECTURE.md` — system design overview
- `docs/INSTALLATION.md` — detailed setup guide
- This changelog
- `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1
- `SECURITY.md` — vulnerability reporting policy
- GitHub issue templates (bug report, feature request, challenge proposal)
- Pull request template
- `--parallel N` flag on `opengym run` for parallel evaluation
- `--verbose` flag on `opengym score` and `opengym run`
- `--csv-output` flag on `opengym score` and `opengym run`
- Per-challenge timing (`duration_seconds`) and cost tracking (`estimated_cost_usd`)
- Progress counters during scoring and running
- Cross-platform CI (Linux, macOS, Windows)
- `--scorecard` flag on `opengym score` and `opengym run` — infra-focused category breakdown
- `challenge_type` field in metadata (`INFRA_CONFORMANCE` / `MODEL_DEPENDENT` / `HYBRID`)
- Infra Conformance Gate — CI enforcement of 5 testability conditions
- Challenge classification system with drift detection rule
- `init-key` command for local/private test encryption keys
- `{repo}` placeholder in `opengym run --agent` templates
- Predefined run profiles for infra benchmarking (`infra-smoke`, `infra-weekly`, `infra-nightly`, `infra-hard`, `safety-gate`)
- `opengym compare` command for report-to-report regression and improvement analysis
- `opengym run --save-report` for metadata-wrapped JSON artifacts with report hashes

### Changed
- `opengym score` now verifies in an isolated staging workspace with canonical hidden tests
- `opengym run` adds `--enforce-scope` (enabled by default) to fail on writes outside `setup/`
- `opengym score` now blocks direct scoring for `INFRA_CONFORMANCE` challenges (must use `opengym run`)
- `opengym run` recreates infra challenge workspaces by default (`--fresh-infra-workspace`) to prevent pre-seeded output cheating
- `opengym run` adds reliability stress controls: `--trials`, `--chaos-level`, and `--chaos-seed` with per-challenge stability reporting
- Fault injection supports step-scoped execution (`fault_injection[].step`)
- Summary output now includes actionable remediation plan entries (`action_plan`)

## [0.2.0] - 2026-03-01

### Added
- 117 new challenges (total: 127) across 7 capability dimensions
- 6 new dimensions: memory, tool-use, resilience, safety, multi-agent, planning
- `opengym run` command with multi-session agent orchestration
- Multi-session challenge support (process killed between steps, workspace cleaned)
- `verify.py` JSON-line test format for infrastructure challenges
- Per-dimension and per-category scoring with diagnostics
- Per-test failure details in summary output (`Failed Challenges:` section)
- Inline failure display during `opengym run`
- Anti-cheat: SHA-256 test integrity verification
- 3 working agent adapters (dummy, OpenAI, Anthropic) in `examples/agents/`
- `docs/AGENT_GUIDE.md` — comprehensive agent integration guide
- `docs/CHALLENGE_SPEC.md` — challenge authoring specification
- CI: metadata validation across all challenges
- PyPI publish workflow via OIDC trusted publisher

### Changed
- Added `dimension` field to all challenge metadata
- Scoring output now includes `by_dimension` breakdown
- `python3` compatibility in verify commands (`sys.executable` fallback)

## [0.1.0] - 2026-02-28

### Added
- Initial release
- CLI with `fetch`, `list`, `score` commands
- 10 challenges (001-010) across 7 categories
- Folder-based challenge format: `README.md`, `setup/`, `tests/`, `metadata.yaml`
- Python CLI with Click (`pip install opengym-ai`)
- Agent-agnostic design: works with any framework
- pytest-based test verification
- JSON output (`--json-output`) for CI integration
- Summary output with diagnostics (`--summary`)
- `CONTRIBUTING.md` — contribution guidelines
