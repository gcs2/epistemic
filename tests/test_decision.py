from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from syntruth.core import ProtocolError
from syntruth.decision import analyze_decision, load_decision, render_decision_markdown, validate_decision


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "library-outreach-decision.json"


class DecisionProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_is_valid(self) -> None:
        validate_decision(self.document)

    def test_missing_impact_cell_is_rejected(self) -> None:
        self.document["impacts"].pop()
        with self.assertRaises(ProtocolError):
            validate_decision(self.document)

    def test_probabilities_must_sum_to_one(self) -> None:
        self.document["worldviews"][0]["scenario_probabilities"]["digital_access_high"] = 0.9
        with self.assertRaises(ProtocolError):
            validate_decision(self.document)

    def test_analysis_is_deterministic(self) -> None:
        first = analyze_decision(self.document)
        second = analyze_decision(self.document)
        self.assertEqual(first, second)

    def test_baseline_scores_zero_in_example(self) -> None:
        result = analyze_decision(self.document)
        self.assertAlmostEqual(result["ensemble_scores"]["current_flyers"], 0.0)

    def test_uncertain_impacts_are_shrunk(self) -> None:
        original = analyze_decision(self.document)["ensemble_scores"]["partner_popups"]
        high_confidence = copy.deepcopy(self.document)
        for impact in high_confidence["impacts"]:
            if impact["option_id"] == "partner_popups":
                impact["confidence"] = 1.0
        revised = analyze_decision(high_confidence)["ensemble_scores"]["partner_popups"]
        self.assertGreater(revised, original)

    def test_uncertain_negative_impacts_disable_robust_label(self) -> None:
        result = analyze_decision(self.document)
        self.assertTrue(result["uncertainty_laundering_cells"])
        self.assertFalse(result["robust_choice"])

    def test_report_keeps_safety_and_learning_visible(self) -> None:
        document = load_decision(EXAMPLE)
        report = render_decision_markdown(document, analyze_decision(document))
        self.assertIn("## Safety and reversibility", report)
        self.assertIn("## Learning contract", report)
        self.assertIn("not authorization", report)


if __name__ == "__main__":
    unittest.main()
