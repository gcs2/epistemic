"""Content-integrity helpers for frozen SES artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .core import ProtocolError


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def verify_manifest(path: str | Path) -> list[dict[str, str | bool]]:
    manifest = Path(path)
    if not manifest.is_file():
        raise ProtocolError(f"Manifest does not exist: {manifest}")
    records: list[dict[str, str | bool]] = []
    for line_number, raw_line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise ProtocolError(f"Malformed manifest line {line_number}")
        expected, relative_name = parts
        target = manifest.parent / relative_name.strip()
        if not target.is_file():
            records.append(
                {
                    "file": str(target),
                    "expected": expected.upper(),
                    "actual": "MISSING",
                    "valid": False,
                }
            )
            continue
        actual = sha256_file(target)
        records.append(
            {
                "file": str(target),
                "expected": expected.upper(),
                "actual": actual,
                "valid": actual == expected.upper(),
            }
        )
    if not records:
        raise ProtocolError("Manifest contains no file records")
    return records
