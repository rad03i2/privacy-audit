# Contributing

Contributions are welcome. Keep the scanner local-first, read-only, dependency-light, and conservative about privacy claims.

1. Fork and create a focused branch.
2. Use Python 3.10+.
3. Install with `python -m pip install -e .`.
4. Run `python -m unittest discover -s tests -v` and `python -m compileall -q src tests`.
5. Add tests for behavior changes.
6. Never commit real secrets, credentials, or personal data; use obviously synthetic fixtures.
7. Open a pull request describing the behavior and privacy impact.

By contributing, you agree that your contribution is licensed under the MIT License.
