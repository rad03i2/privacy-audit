# Changelog

All notable project changes are documented here.

## Unreleased

### Repository presentation

- Added a dedicated Privacy Lens / Redaction Signal visual identity.
- Added canonical project cover and square logo assets.
- Reorganized the main README around actual scanner behavior, local privacy boundaries, rules, CI, and limitations.
- Added separate English and Arabic guides.
- Added architecture and brand documentation.
- Expanded security/privacy and contribution guidance.
- Added repository collaboration templates and a clearly separated roadmap.

No scanner rules, CLI behavior, or runtime logic were changed by this identity and documentation refresh.

## 1.0.0

Initial public release.

### Included

- Local recursive text scanning.
- UTF-8 / UTF-8 BOM handling.
- Email and IPv4 signals.
- Private-key, AWS-style access-key, GitHub-token, and generic credential-like patterns.
- Low, medium, and high severities.
- Redacted excerpts.
- Binary/oversized/undecodable-file skipping.
- Symlink exclusion.
- Human-readable and JSON output.
- `--fail-on` CI thresholds.
- Python API and module entry point.
- Cross-platform GitHub Actions test matrix.
