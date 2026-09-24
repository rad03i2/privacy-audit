"""Command-line interface for Privacy Audit."""
from __future__ import annotations

import argparse
import json
import sys
from . import __version__
from .scanner import scan_path

SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="privacy-audit", description="Read-only local privacy scanner")
    p.add_argument("path", nargs="?", help="File or directory to scan")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p.add_argument("--max-bytes", type=int, default=2_000_000, help="Maximum file size to inspect")
    p.add_argument("--fail-on", choices=("low", "medium", "high"), help="Exit 2 when this severity or higher is found")
    p.add_argument("--version", action="version", version=f"privacy-audit {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.path:
        build_parser().print_help()
        return 0
    try:
        findings, summary = scan_path(args.path, args.max_bytes)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"summary": summary, "findings": [f.to_dict() for f in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Scanned: {summary['scanned_files']} | Skipped: {summary['skipped_files']} | Findings: {summary['findings']}")
        for f in findings:
            print(f"[{f.severity.upper():6}] {f.path}:{f.line} {f.rule} — {f.message} — {f.excerpt}")
    if args.fail_on:
        threshold = SEVERITY_RANK[args.fail_on]
        if any(SEVERITY_RANK[f.severity] >= threshold for f in findings):
            return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
