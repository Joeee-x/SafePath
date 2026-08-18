"""Fail fast when the public portfolio contains obvious private material."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_EXTENSIONS = {".md", ".py", ".json", ".txt", ".yml", ".yaml"}
BLOCKED_PATH_PARTS = {".git", ".venv", "venv", "__pycache__"}
FORBIDDEN_PATTERNS = {
    "local Windows path": re.compile(r"[A-Za-z]:\\\\(?:Users|Documents)\\", re.IGNORECASE),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credential assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\\s*[:=]\\s*[^\\s]{8,}"),
    "telephone number": re.compile(r"(?<![\d-])(?:1\d{10}|0\d{2,3}-?\d{7,8})(?!\d)"),
    "external URL": re.compile(r"https?://", re.IGNORECASE),
}


def iter_public_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_EXTENSIONS
        and path != Path(__file__).resolve()
        and not any(part in BLOCKED_PATH_PARTS for part in path.parts)
    ]


def validate_demo_data() -> list[str]:
    errors: list[str] = []
    payload = json.loads((ROOT / "data" / "demo_records.json").read_text(encoding="utf-8"))
    if payload.get("data_classification") != "synthetic_demo_only":
        errors.append("demo_records.json is not explicitly marked synthetic_demo_only")
    forbidden_fields = {"address", "contact", "phone", "website", "source_url", "notes"}
    for index, record in enumerate(payload.get("records", []), start=1):
        overlap = forbidden_fields.intersection(record)
        if overlap:
            errors.append(f"demo record {index} includes forbidden fields: {sorted(overlap)}")
    return errors


def main() -> int:
    errors = validate_demo_data()
    for path in iter_public_text_files():
        text = path.read_text(encoding="utf-8")
        for name, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: possible {name}")

    if errors:
        print("Public-release validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Public-release validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
