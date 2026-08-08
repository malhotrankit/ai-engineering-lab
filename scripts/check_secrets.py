#!/usr/bin/env python3
"""Fail safely when repository files appear to contain credentials.

The scanner reports only a path, line number, and rule name. It never prints the
matched value. Ignored files such as local .env files are deliberately excluded.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_TEXT_FILE_BYTES = 5_000_000

SECRET_PATTERNS = (
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("OpenRouter API key", re.compile(r"\bsk-or-v1-[0-9A-Za-z_-]{20,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[0-9A-Za-z_-]{20,}\b")),
    ("OpenAI-style API key", re.compile(r"\bsk-(?:proj-)?[0-9A-Za-z_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b")),
    ("AWS access-key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "Private-key material",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
)

GENERIC_SECRET_ASSIGNMENT = re.compile(
    r"\b[A-Z][A-Z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD)\s*=\s*([^\s#]+)"
)

PLACEHOLDER_MARKERS = (
    "your-",
    "replace",
    "placeholder",
    "example",
    "dummy",
    "changeme",
    "not-a-real",
    "test-only",
    "os.getenv",
    "os.environ",
    "${",
    "<",
)


def repository_paths() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / raw.decode() for raw in result.stdout.split(b"\0") if raw]


def has_sensitive_path(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    lower_name = path.name.lower()
    if lower_name == ".env" or (lower_name.startswith(".env.") and lower_name != ".env.example"):
        return True
    if path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
        return True
    return lower_name.startswith(("credentials", "service-account", "secrets."))


def is_safe_assignment(value: str) -> bool:
    normalized = value.strip().strip("'\"").lower()
    if not normalized or normalized in {"none", "null", "''", '""'}:
        return True
    return any(marker in normalized for marker in PLACEHOLDER_MARKERS)


def scan_text(path: Path, text: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule_name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append((line_number, rule_name))

        assignment = GENERIC_SECRET_ASSIGNMENT.search(line)
        if assignment and not is_safe_assignment(assignment.group(1)):
            findings.append((line_number, "Hardcoded secret-like assignment"))
    return findings


def main() -> int:
    findings: list[tuple[Path, int, str]] = []
    for path in repository_paths():
        if not path.is_file():
            continue
        if has_sensitive_path(path):
            findings.append((path, 0, "Sensitive filename is tracked or unignored"))
            continue
        if path.stat().st_size > MAX_TEXT_FILE_BYTES:
            continue

        raw = path.read_bytes()
        if b"\0" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        for line_number, rule_name in scan_text(path, text):
            findings.append((path, line_number, rule_name))

    if findings:
        print("Secret scan failed. No suspected values are displayed.")
        for path, line_number, rule_name in findings:
            relative = path.relative_to(ROOT)
            location = f"{relative}:{line_number}" if line_number else str(relative)
            print(f"- {location}: {rule_name}")
        print("Revoke/rotate any real exposed credential before continuing.")
        return 1

    print("Secret scan passed: no credential patterns found in tracked or unignored files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
