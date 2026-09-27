# Security and Privacy Policy

## Supported version

Security and privacy fixes target the latest code on the default branch and the latest tagged release when applicable.

## Design boundary

Privacy Audit is a **local, read-only, heuristic text scanner**.

The current implementation:

- reads local files;
- does not modify scanned content;
- does not intentionally persist scanned file contents;
- does not make network requests;
- does not require an account, API key, token, or telemetry endpoint;
- does not follow symbolic-link targets;
- skips common generated/dependency directories during directory scans;
- redacts excerpts before displaying findings.

## Reports are still sensitive

Redaction reduces accidental echoing of a full matched value, but it does not make reports automatically safe to publish.

A report can expose:

- filenames and directory structure;
- line numbers;
- the type and severity of a detected pattern;
- partial surrounding context.

Treat scan output as potentially sensitive review material.

## Heuristic limitations

A finding is not proof that:

- an address belongs to a specific person;
- a credential is valid;
- a key has been compromised;
- a privacy law or policy has been violated.

A clean scan is also not proof that content contains no sensitive data.

False positives and false negatives are expected in any pattern-based scanner.

## Out-of-scope content

The current scanner does not inspect the semantic content of:

- archives;
- images;
- PDFs as structured documents;
- Office documents;
- Git history;
- remote repositories;
- cloud services;
- databases.

Binary or non-UTF-8 content can be skipped.

## Test and issue safety

Never use real credentials, access tokens, private keys, private customer data, or personally identifying information in tests, examples, screenshots, issues, or pull requests.

Use obviously synthetic fixtures.

## Reporting a security issue

Prefer GitHub private security reporting when available.

Include:

- affected version or commit;
- operating system and Python version;
- a minimal synthetic reproduction;
- expected behavior;
- observed behavior;
- privacy/security impact;
- sanitized logs if helpful.

Do not publish real secrets or personal data in a public issue.
