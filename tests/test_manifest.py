import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
ENGINE = MODEL_DIR / "eo_detector_fp16.engine"
MANIFEST = MODEL_DIR / "manifest.json"


class ManifestTests(unittest.TestCase):
    def test_engine_exists_and_is_not_empty(self):
        self.assertTrue(ENGINE.is_file())
        self.assertGreater(ENGINE.stat().st_size, 0)

    def test_manifest_exists_and_is_valid(self):
        self.assertTrue(MANIFEST.is_file())
        with MANIFEST.open(encoding="utf-8") as file:
            manifest = json.load(file)
        for field in (
            "model_name", "version", "target_arch",
            "input_resolution", "precision", "sha256"
        ):
            self.assertIn(field, manifest)

    def test_engine_checksum_matches_manifest(self):
        with MANIFEST.open(encoding="utf-8") as file:
            manifest = json.load(file)

        digest = hashlib.sha256()
        with ENGINE.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)

        self.assertEqual(
            digest.hexdigest(),
            manifest["sha256"].lower()
        )


if __name__ == "__main__":
    unittest.main()
