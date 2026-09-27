## Summary

Describe the problem and the proposed change.

## Privacy / behavior impact

- [ ] The scanner remains local and read-only, or the boundary change is explained below.
- [ ] No hidden network access or telemetry was introduced.
- [ ] Findings remain clearly heuristic rather than definitive identity/compromise claims.
- [ ] Sensitive context is still redacted before display.
- [ ] Tests use synthetic data only.

## Validation

- [ ] `python -m compileall -q src tests`
- [ ] `python -m unittest discover -s tests -v`
- [ ] `privacy-audit --version`
- [ ] User-facing documentation was updated when needed.
- [ ] No real tokens, credentials, personal data, or private files are included.

## Notes

Add compatibility, false-positive, false-negative, or privacy context reviewers should know.
