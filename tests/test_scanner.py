import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from privacy_audit.cli import main
from privacy_audit.scanner import scan_path, scan_text

class ScannerTests(unittest.TestCase):
    def test_detects_and_redacts_secret(self):
        found = scan_text('api_key = "abcdefgh12345678"')
        self.assertEqual(found[0].rule, "generic-secret")
        self.assertNotIn("abcdefgh12345678", found[0].excerpt)

    def test_detects_email_and_private_key(self):
        found = scan_text("owner@example.com\n-----BEGIN PRIVATE KEY-----")
        self.assertEqual({x.rule for x in found}, {"email", "private-key"})

    def test_utf8_and_skips_binary(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "arabic.txt").write_text("البريد test@example.com", encoding="utf-8")
            (root / "blob.bin").write_bytes(b"abc\x00def")
            findings, summary = scan_path(root)
            self.assertEqual(len(findings), 1)
            self.assertEqual(summary["scanned_files"], 1)
            self.assertEqual(summary["skipped_files"], 1)

    def test_size_limit(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "large.txt"
            p.write_text("x" * 20)
            findings, summary = scan_path(p, max_bytes=5)
            self.assertFalse(findings)
            self.assertEqual(summary["skipped_files"], 1)

    def test_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            scan_path("definitely-not-here-privacy-audit")

    def test_cli_fail_threshold(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "x.txt"
            p.write_text("hello a@example.com")
            self.assertEqual(main([str(p), "--fail-on", "high"]), 0)
            self.assertEqual(main([str(p), "--fail-on", "low"]), 2)

if __name__ == "__main__":
    unittest.main()
