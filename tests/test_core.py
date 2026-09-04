from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from syntruth.core import ProtocolError, analyze, ensemble_posterior, load_inquiry, render_markdown, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anschluss.json"


class ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_is_valid(self) -> None:
        validate(self.document)

    def test_missing_likelihood_is_rejected(self) -> None:
        del self.document["evidence"][0]["likelihoods"]["germany_loses_austria"]
        with self.assertRaises(ProtocolError):
            validate(self.document)

    def test_posteriors_sum_to_one(self) -> None:
        result = analyze(self.document)
        self.assertAlmostEqual(sum(result["ensemble"].values()), 1.0)
        for distribution in result["per_model"].values():
            self.assertAlmostEqual(sum(distribution.values()), 1.0)

    def test_correlated_duplicate_does_not_multiply_signal(self) -> None:
        baseline, _ = ensemble_posterior(self.document)
        duplicate = copy.deepcopy(self.document["evidence"][0])
        duplicate["id"] = "foreign_nonintervention_duplicate"
        self.document["evidence"].append(duplicate)
        repeated, _ = ensemble_posterior(self.document)
        for hypothesis_id in baseline:
            self.assertAlmostEqual(baseline[hypothesis_id], repeated[hypothesis_id])

    def test_independent_duplicate_increases_signal(self) -> None:
        baseline, _ = ensemble_posterior(self.document)
        duplicate = copy.deepcopy(self.document["evidence"][0])
        duplicate["id"] = "foreign_nonintervention_independent"
        duplicate["independence_group"] = "independent_replication"
        self.document["evidence"].append(duplicate)
        repeated, _ = ensemble_posterior(self.document)
        self.assertGreater(
            repeated["hitler_regime_retains"],
            baseline["hitler_regime_retains"],
        )

    def test_robustness_is_deterministic(self) -> None:
        first = analyze(self.document)["robustness"]
        second = analyze(self.document)["robustness"]
        self.assertEqual(first, second)

    def test_markdown_report_contains_epistemic_sections(self) -> None:
        document = load_inquiry(EXAMPLE)
        report = render_markdown(document, analyze(document))
        self.assertIn("## Evidence leverage", report)
        self.assertIn("## Registered challenges", report)
        self.assertIn("## Declared limitations", report)


if __name__ == "__main__":
    unittest.main()
