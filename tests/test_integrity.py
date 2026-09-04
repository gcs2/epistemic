from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from syntruth.core import ProtocolError
from syntruth.integrity import verify_manifest


class IntegrityTests(unittest.TestCase):
    def test_valid_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "artifact.txt"
            target.write_text("frozen", encoding="utf-8")
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest = root / "MANIFEST.sha256"
            manifest.write_text(f"{digest}  artifact.txt\n", encoding="utf-8")
            records = verify_manifest(manifest)
            self.assertTrue(records[0]["valid"])

    def test_modified_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "artifact.txt"
            target.write_text("before", encoding="utf-8")
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest = root / "MANIFEST.sha256"
            manifest.write_text(f"{digest}  artifact.txt\n", encoding="utf-8")
            target.write_text("after", encoding="utf-8")
            records = verify_manifest(manifest)
            self.assertFalse(records[0]["valid"])

    def test_empty_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "MANIFEST.sha256"
            manifest.write_text("# empty\n", encoding="utf-8")
            with self.assertRaises(ProtocolError):
                verify_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
