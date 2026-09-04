from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from syntruth.benchmark import run_benchmark, validate_benchmark_config, write_benchmark_outputs
from syntruth.core import ProtocolError


def small_config() -> dict:
    return {
        "experiment_id": "test",
        "title": "Test benchmark",
        "seed": 11,
        "bootstrap_seed": 12,
        "trials_per_cell": 120,
        "groups": [3],
        "max_duplicates": [1, 4],
        "rho": [0.0, 1.0],
        "signal_strength": [0.5],
        "sigma": 1.0,
        "base_rate": 0.5,
        "rho_estimation_sd": 0.1,
        "bootstrap_samples": 100,
        "methods": ["oracle", "estimated", "conservative", "naive", "one_per_group"],
    }


class BenchmarkTests(unittest.TestCase):
    def test_small_config_is_valid(self) -> None:
        validate_benchmark_config(small_config())

    def test_invalid_method_is_rejected(self) -> None:
        config = small_config()
        config["methods"].append("alchemy")
        with self.assertRaises(ProtocolError):
            validate_benchmark_config(config)

    def test_run_is_deterministic(self) -> None:
        first = run_benchmark(small_config())
        second = run_benchmark(small_config())
        self.assertEqual(first, second)

    def test_no_duplication_methods_are_equivalent(self) -> None:
        result = run_benchmark(small_config())
        h6 = next(item for item in result["hypotheses"] if item["id"] == "H6")
        self.assertTrue(h6["supported"])
        self.assertLessEqual(h6["effect"], 1e-12)

    def test_perfect_correlation_oracle_equals_conservative(self) -> None:
        config = small_config()
        config["max_duplicates"] = [4]
        config["rho"] = [1.0]
        result = run_benchmark(config)
        rows = {row["method"]: row for row in result["rows"]}
        self.assertAlmostEqual(rows["oracle"]["brier"], rows["conservative"]["brier"])
        self.assertAlmostEqual(rows["oracle"]["log_loss"], rows["conservative"]["log_loss"])

    def test_outputs_are_created(self) -> None:
        result = run_benchmark(small_config())
        with tempfile.TemporaryDirectory() as directory:
            paths = write_benchmark_outputs(result, directory)
            self.assertTrue(all(path.exists() for path in paths.values()))
            summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
            self.assertNotIn("rows", summary)


if __name__ == "__main__":
    unittest.main()
