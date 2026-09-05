"""Portable repository checks; no external dependencies or writes."""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from syntruth.integrity import verify_manifest


def main():
    failures = []
    files = [p for p in ROOT.rglob("*") if p.is_file()
             and not any(part in {".git", "work", "__pycache__", ".venv", "build", "dist"}
                         for part in p.relative_to(ROOT).parts)]
    counts = {"json": 0, "markdown": 0, "manifests": 0}
    for path in files:
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
                counts["json"] += 1
            except (ValueError, UnicodeError) as exc:
                failures.append(f"{path}: {exc}")
        elif path.suffix == ".md":
            counts["markdown"] += 1
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = target.strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                if not (path.parent / unquote(target)).exists():
                    failures.append(f"{path.relative_to(ROOT)}: missing link {target}")
        elif path.name == "MANIFEST.sha256" or path.name.endswith("FROZEN.sha256"):
            counts["manifests"] += 1
            for record in verify_manifest(path):
                if not record["valid"]:
                    failures.append(f"Hash mismatch: {record['file']}")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = project["project"]["version"]
    from syntruth import __version__
    if version != __version__ or f"**Version:** {version}" not in (ROOT / "STATUS.md").read_text(encoding="utf-8"):
        failures.append("Package and status versions disagree")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"Repository checks passed: {counts}; version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

