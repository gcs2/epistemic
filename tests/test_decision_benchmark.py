from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from syntruth.core import ProtocolError
from syntruth.decision_benchmark import (
    load_decision_benchmark_config,
    run_decision_benchmark,
    validate_decision_benchmark_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "experiments" / "003a-decision-stress" / "config.json"


class DecisionBenchmarkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.config["cases_per_cell"] = 8
        self.config["bootstrap_samples"] = 0
        self.config["sensitivity_samples"] = 5
        for field in (
            "tail_probability", "tail_visibility", "probability_error", "impact_error",
            "value_shift", "negative_impact_confidence",
        ):
            self.config[field] = [self.config[field][-1]]

    def test_small_config_is_valid(self) -> None:
        validate_decision_benchmark_config(self.config)

    def test_unknown_method_is_rejected(self) -> None:
        self.config["methods"].append("omniscient_vibes")
        with self.assertRaises(ProtocolError):
            validate_decision_benchmark_config(self.config)

    def test_small_run_is_deterministic(self) -> None:
        self.assertEqual(run_decision_benchmark(self.config), run_decision_benchmark(self.config))

    def test_oracle_has_zero_regret(self) -> None:
        result = run_decision_benchmark(self.config)
        self.assertAlmostEqual(result["aggregate"]["oracle_expected"]["mean_regret"], 0.0)

    def test_omitted_tail_config_executes(self) -> None:
        self.config["tail_visibility"] = ["omitted"]
        result = run_decision_benchmark(self.config)
        self.assertEqual(result["cells"], 1)

    def test_loader_records_config_hash(self) -> None:
        config = load_decision_benchmark_config(CONFIG)
        self.assertEqual(len(config["_config_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
