"""Local, read-only privacy scanning primitives."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Iterable

MAX_DEFAULT_BYTES = 2_000_000

@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    severity: str
    message: str
    excerpt: str

    def to_dict(self) -> dict:
        return asdict(self)

# Deliberately conservative: useful signals without pretending to prove identity.
RULES = (
    ("email", "low", re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.I), "Possible email address"),
    ("ipv4", "low", re.compile(r"(?<!\d)(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?!\d)"), "IPv4 address"),
    ("private-key", "high", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "Private key material"),
    ("aws-access-key", "high", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "AWS-style access key identifier"),
    ("github-token", "high", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,255}\b"), "GitHub-style token"),
    ("generic-secret", "medium", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?([^\s'\"]{8,})"), "Possible embedded credential"),
)

IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}


def _redact(text: str, limit: int = 100) -> str:
    text = text.strip().replace("\t", " ")
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    # Excerpts should help locate a finding without echoing full secrets.
    if len(text) <= 8:
        return "***"
    return text[:4] + "…" + text[-4:]


def scan_text(text: str, path: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(text.splitlines(), 1):
        for rule, severity, pattern, message in RULES:
            if pattern.search(line):
                findings.append(Finding(path, number, rule, severity, message, _redact(line)))
    return findings


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


def scan_path(target: str | Path, max_bytes: int = MAX_DEFAULT_BYTES) -> tuple[list[Finding], dict]:
    root = Path(target)
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if root.is_symlink():
        raise ValueError("Symbolic-link targets are not scanned")
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")
    findings: list[Finding] = []
    scanned = skipped = 0
    for path in iter_files(root):
        try:
            if path.stat().st_size > max_bytes:
                skipped += 1
                continue
            raw = path.read_bytes()
            if b"\x00" in raw[:4096]:
                skipped += 1
                continue
            text = raw.decode("utf-8-sig")
        except (OSError, UnicodeDecodeError):
            skipped += 1
            continue
        scanned += 1
        findings.extend(scan_text(text, str(path)))
    summary = {"scanned_files": scanned, "skipped_files": skipped, "findings": len(findings)}
    return findings, summary
