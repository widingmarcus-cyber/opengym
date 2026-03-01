# Contributing to OpenGym

We welcome contributions! The easiest way to help is to add new challenges.

## Adding a Challenge

1. Fork the repo
2. Create a folder: `challenges/NNN-your-challenge-name/`
3. Follow the structure in [docs/CHALLENGE_SPEC.md](docs/CHALLENGE_SPEC.md)
4. Verify your challenge works:
   - Tests **fail** before the fix
   - Tests **pass** after the fix
   - No internet required
   - No hints in the source code
5. Submit a PR

## Challenge Quality Checklist

- [ ] `README.md` clearly describes the task
- [ ] `metadata.yaml` has all required fields
- [ ] Tests are deterministic (no randomness)
- [ ] Tests cover edge cases
- [ ] Source code has **no comments hinting at the solution**
- [ ] Challenge works offline
- [ ] Agent only needs to modify files in `setup/`

## Code Contributions

For CLI or infrastructure changes:

1. Fork the repo
2. Install dev dependencies: `pip install -e .`
3. Make your changes
4. Test: `opengym list` and `opengym score` still work
5. Submit a PR

## Reporting Issues

Open an issue on GitHub with:
- What you expected
- What happened
- Steps to reproduce
