# Privacy Audit — English Guide

Privacy Audit is a dependency-free Python command-line scanner for reviewing UTF-8 text files and source trees for patterns that may expose privacy-sensitive or credential-like material.

It runs locally, does not modify scanned files, and reports redacted findings designed for human review or lightweight CI gating.

> Current release: **1.0.0** · Python **3.10+** · License **MIT**

## Installation

```bash
git clone https://github.com/rad03i2/privacy-audit.git
cd privacy-audit
python -m pip install .
```

For editable development installation:

```bash
python -m pip install -e .
```

## Basic usage

Scan a directory:

```bash
privacy-audit ./project
```

Scan one text file:

```bash
privacy-audit notes.txt
```

Emit JSON:

```bash
privacy-audit ./project --json
```

Fail when medium-or-higher signals exist:

```bash
privacy-audit . --fail-on medium
```

Change the maximum inspected file size:

```bash
privacy-audit . --max-bytes 500000
```

The module entry point is also supported:

```bash
python -m privacy_audit ./project
```

## Current rules

| Rule | Severity | Description |
|---|---|---|
| `email` | low | Possible email address |
| `ipv4` | low | IPv4 address |
| `generic-secret` | medium | Credential-like value assigned to an API-key/secret/token/password label |
| `private-key` | high | Private-key header |
| `aws-access-key` | high | AWS-style access-key identifier |
| `github-token` | high | GitHub-style token pattern |

These checks are heuristic. Review a finding before deciding whether it is genuinely sensitive.

## Output

Human-readable output includes:

- severity;
- file path;
- line number;
- rule;
- message;
- a shortened, partially redacted excerpt.

JSON output contains:

```json
{
  "summary": {
    "scanned_files": 0,
    "skipped_files": 0,
    "findings": 0
  },
  "findings": []
}
```

The values above only illustrate the schema.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Scan completed and threshold was not reached |
| `1` | Invalid input/read-related failure |
| `2` | `--fail-on` threshold reached |

## File handling

The scanner:

- accepts one file or recursively scans a directory;
- skips symbolic links;
- skips common generated/dependency directories;
- skips files larger than the configured limit;
- skips likely binary files when a NUL byte appears near the beginning;
- decodes text with `utf-8-sig`;
- skips undecodable files.

The default file-size limit is 2,000,000 bytes.

## Python API

```python
from privacy_audit import scan_path, scan_text

findings, summary = scan_path("./project")

for finding in findings:
    print(
        finding.rule,
        finding.severity,
        finding.path,
        finding.line,
    )

inline = scan_text("Contact: person@example.com")
```

## Privacy model

Privacy Audit is designed to keep inspected content local.

The scanner has no runtime dependencies and its implementation does not make network requests. It does not modify scanned files or intentionally persist scanned content.

Generated reports may still be sensitive. A path, line number, rule name, and redacted excerpt can reveal useful context, so report output should be handled carefully.

See [SECURITY.md](SECURITY.md).

## Testing

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
privacy-audit --version
```

The CI matrix runs on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Limitations

Privacy Audit is not a DLP platform, secret manager, malware scanner, or compliance/certification product.

False positives and false negatives are possible. The current scanner does not inspect binary document formats, archives, images, PDFs as structured documents, Office files, Git history, or remote services.

A clean result is not proof that a project contains no personal or secret information.

## More documentation

- [Main project page](README.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security](SECURITY.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Brand system](docs/BRAND.md)

---

**Developer:** Radwan Abd alhady Ahmed · [@rad03i2](https://github.com/rad03i2)
