# Contributing to Privacy Audit

Contributions are welcome when they preserve the project's local-first, read-only, dependency-light design.

## Development setup

Use Python 3.10 or newer.

```bash
git clone https://github.com/rad03i2/privacy-audit.git
cd privacy-audit
python -m pip install -e .
```

## Validation

Run:

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
privacy-audit --version
```

Behavior changes should include focused tests.

## Privacy rules for contributions

Do not commit or paste:

- real access tokens;
- API keys;
- private keys;
- customer data;
- private email addresses;
- private IP inventories;
- personal documents;
- production logs containing sensitive content.

Use synthetic examples that are obviously non-production.

## Scanner design principles

Changes should preserve these properties unless a proposal explicitly explains and justifies a boundary change:

- local processing;
- read-only scanning;
- no hidden network calls;
- no telemetry;
- no silent content modification;
- no symlink traversal;
- understandable rule names;
- findings that are clearly presented as heuristic signals;
- redaction before matching context is displayed.

## Adding or changing rules

A detector change should explain:

1. what signal the rule detects;
2. why the severity is appropriate;
3. likely false-positive cases;
4. likely false-negative cases;
5. synthetic test coverage;
6. whether output could reveal more sensitive context.

Avoid rules that make identity, compromise, or compliance claims the scanner cannot establish.

## Pull requests

Prefer small, reviewable pull requests. Include:

- the problem being solved;
- the behavior change;
- tests;
- documentation changes when user-facing behavior changes;
- privacy impact, if any.

The repository pull-request template includes a short safety checklist.

## Maintainer

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed** · [@rad03i2](https://github.com/rad03i2)

Contributions are provided under the repository's MIT License.
