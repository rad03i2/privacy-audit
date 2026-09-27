# Architecture

Privacy Audit is intentionally compact and dependency-free at runtime. The code is split between a scanning core and a thin command-line layer.

## Component map

```text
CLI
src/privacy_audit/cli.py
        │
        ▼
scan_path(target, max_bytes)
        │
        ├── iter_files(...)
        │      ├── skip symlinks
        │      └── skip common generated/dependency directories
        │
        ▼
read bytes locally
        │
        ├── skip oversized files
        ├── skip likely binary files
        └── decode UTF-8 / UTF-8 BOM
        │
        ▼
scan_text(...)
        │
        └── conservative regex rules
        │
        ▼
Finding objects + summary
        │
        ├── human-readable CLI
        └── JSON output
```

## Scanner core

`src/privacy_audit/scanner.py` owns the read-only scanning behavior.

### Current rule set

| Rule | Severity | Signal |
|---|---|---|
| `email` | low | Possible email address |
| `ipv4` | low | IPv4 address |
| `private-key` | high | Private-key header |
| `aws-access-key` | high | AWS-style access-key identifier |
| `github-token` | high | GitHub-style token |
| `generic-secret` | medium | Credential-like assignment such as token/password/secret/API key |

These rules are heuristics. A match is a signal for review, not proof of identity, compromise, or policy violation.

## File traversal

`iter_files` accepts either a single file or a directory tree.

For directory scans it:

- recursively enumerates files;
- does not follow symbolic links;
- skips files under common directories such as `.git`, `.venv`, `venv`, `node_modules`, `dist`, `build`, and `__pycache__`.

## Text boundary

For each candidate file, `scan_path`:

1. checks the configured size limit;
2. reads bytes locally;
3. treats a NUL byte in the first 4096 bytes as a binary signal and skips the file;
4. decodes with `utf-8-sig`;
5. skips undecodable files;
6. passes decoded text to `scan_text`.

The default file-size ceiling is 2,000,000 bytes.

## Findings and redaction

A finding contains:

- path;
- line number;
- rule name;
- severity;
- explanation;
- a redacted excerpt.

The excerpt is intentionally shortened and partially hidden. This reduces accidental secret echoing, but output should still be treated as potentially sensitive.

## CLI layer

`src/privacy_audit/cli.py` provides:

- human-readable output;
- `--json`;
- `--max-bytes`;
- `--fail-on low|medium|high`;
- `--version`.

Exit behavior:

| Code | Meaning |
|---|---|
| `0` | Scan completed and configured threshold was not reached |
| `1` | Invalid target/read-related input failure |
| `2` | Configured `--fail-on` threshold was reached |

## Trust and privacy boundary

Privacy Audit does not:

- make network requests;
- upload scanned files;
- modify scanned content;
- intentionally persist file contents;
- follow symbolic-link targets.

It also does not prove that a clean tree contains no sensitive data. Binary formats, archives, images, PDFs, Office documents, Git history, and remote services are outside the current scanner.

## Tests

`tests/test_scanner.py` covers:

- secret detection with redaction;
- email and private-key detection;
- UTF-8 text scanning;
- binary skipping;
- file-size limits;
- invalid paths;
- CLI failure thresholds.

GitHub Actions installs the package, compiles source/tests, runs the unittest suite, and executes a CLI version smoke test on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.
