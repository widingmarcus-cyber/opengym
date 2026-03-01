# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | Yes       |
| < 0.2   | No        |

## Reporting a Vulnerability

**Do NOT open a public issue for security vulnerabilities.**

Instead, use [GitHub's private vulnerability reporting](https://github.com/widingmarcus-cyber/opengym/security/advisories/new) or contact the maintainers directly.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

**Response timeline:**
- Acknowledge within 48 hours
- Provide an initial assessment within 7 days
- Patch critical issues within 14 days

## Scope

In scope:
- CLI code in `cli/`
- Test integrity verification (anti-cheat)
- Agent adapter examples in `examples/agents/`
- CI/CD workflows

Out of scope:
- Agent code that users write themselves
- LLM API security (responsibility of the API provider)
- Challenge solutions (these are meant to be solved)

## Agent Safety

OpenGym challenges run locally on your machine. The CLI never makes network calls. If you're running untrusted agents, use a sandbox (Docker, VM, etc.). See the README's Safety section.
