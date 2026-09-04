from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from syntruth.core import ProtocolError
from syntruth.decision_v2 import (
    analyze_decision_v2,
    load_decision_v2,
    render_decision_v2_markdown,
    validate_decision_v2,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "library-outreach-bda.json"


class BoundedDecisionAssuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def setUp(self) -> None:
        self.packet = copy.deepcopy(self.document)

    def test_example_is_valid(self) -> None:
        validate_decision_v2(self.packet)

    def test_analysis_is_deterministic(self) -> None:
        first = analyze_decision_v2(self.packet)
        second = analyze_decision_v2(self.packet)
        self.assertEqual(first, second)

    def test_missing_consequence_is_rejected(self) -> None:
        self.packet["consequences"].pop()
        with self.assertRaises(ProtocolError):
            validate_decision_v2(self.packet)

    def test_reversed_consequence_range_is_rejected(self) -> None:
        self.packet["consequences"][8]["estimate"] = {
            "low": 60,
            "central": 55,
            "high": 20,
        }
        with self.assertRaises(ProtocolError):
            validate_decision_v2(self.packet)

    def test_evidence_quality_does_not_shrink_signed_consequences(self) -> None:
        original = analyze_decision_v2(self.packet)
        changed = copy.deepcopy(self.packet)
        for evidence in changed["evidence"]:
            if evidence["id"] == "e_residents":
                evidence["quality"] = "unknown"
        revised = analyze_decision_v2(changed)
        self.assertEqual(original["option_results"], revised["option_results"])
        self.assertFalse(original["analysis_contract"]["evidence_in_arithmetic"])

    def test_open_blocker_deficit_blocks_status(self) -> None:
        for deficit in self.packet["deficits"]:
            if deficit["id"] == "d_real_data":
                deficit["status"] = "open"
        result = analyze_decision_v2(self.packet)
        self.assertEqual(result["assurance_case"]["status"], "blocked")
        self.assertTrue(
            any("d_real_data" in item for item in result["assurance_case"]["blockers"])
        )

    def test_missing_required_challenge_blocks_status(self) -> None:
        self.packet["assurance"]["required_challenge_types"].append("adversarial")
        result = analyze_decision_v2(self.packet)
        self.assertEqual(result["assurance_case"]["status"], "blocked")
        self.assertEqual(result["assurance_case"]["missing_challenge_types"], ["adversarial"])

    def test_constraint_violation_blocks_candidate(self) -> None:
        self.packet["constraints"][0]["threshold"] = 100
        result = analyze_decision_v2(self.packet)
        self.assertEqual(result["assurance_case"]["status"], "blocked")
        self.assertTrue(
            any("underserved_floor" in item for item in result["assurance_case"]["blockers"])
        )

    def test_report_states_bounded_semantics(self) -> None:
        document = load_decision_v2(EXAMPLE)
        report = render_decision_v2_markdown(document, analyze_decision_v2(document))
        self.assertIn("## Assurance case", report)
        self.assertIn("## Evidence boundary", report)
        self.assertIn("not a universal robustness guarantee", report)
        self.assertIn("not authorization", report)
        self.assertIn("is not multiplied into consequence magnitude", report)


if __name__ == "__main__":
    unittest.main()
