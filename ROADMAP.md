# Roadmap

Privacy Audit keeps future ideas separate from features that exist today.

Everything below is a **candidate direction**, not an implemented feature or release promise.

## Candidate ideas

### Opt-in custom rules

Explore a documented way to add project-specific text patterns without changing the built-in conservative rule set.

### Ignore configuration

Explore an explicit ignore file for intentionally excluded paths or known-safe patterns.

Any ignore mechanism should be easy to audit and should avoid silently suppressing broad classes of findings.

### SARIF export

Explore a structured SARIF output mode for security-oriented CI integrations.

### Additional structured-text detectors

Consider narrowly scoped detectors where the signal can be explained and tested without implying identity or compromise.

## Design constraints

Future changes should preserve:

- local processing by default;
- read-only behavior;
- no hidden telemetry or upload;
- understandable rule names;
- redacted output;
- transparent false-positive/false-negative limitations;
- a clear distinction between a detected pattern and a confirmed privacy/security incident.

The roadmap does not currently commit to binary document parsing, cloud scanning, automatic remediation, compliance scoring, or secret revocation.
