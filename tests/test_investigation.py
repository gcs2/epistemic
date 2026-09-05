from __future__ import annotations

import copy
import unittest

from syntruth.core import ProtocolError
from syntruth.investigation import choose, outcome_metrics, replay, terminal, update, validate
from syntruth.investigation_benchmark import make_case, actual_case


class InvestigationTests(unittest.TestCase):
    def setUp(self):
        self.packet = make_case(123)
        self.weights = {"public": 1.0}

    def test_exact_tail_includes_fraction_of_boundary_atom(self):
        atoms = [{"p": .99, "scores": {"public": 10}},
                 {"p": .01, "scores": {"public": -100}}]
        metrics = outcome_metrics(atoms, self.weights)
        self.assertAlmostEqual(metrics["expected_utility"], 8.9)
        self.assertAlmostEqual(metrics["outcome_lower_tail_mean"], -12)
        self.assertAlmostEqual(metrics["severe_loss_probability"], .01)

    def test_constant_outcome_has_constant_tail(self):
        self.assertEqual(outcome_metrics([{"p": 1, "scores": {"public": -7}}], self.weights)
                         ["outcome_lower_tail_mean"], -7)

    def test_invalid_distribution_and_nonfinite_values_rejected(self):
        for p, value in ((.9, 1), (1, float("nan")), (1, True)):
            with self.subTest(p=p, value=value), self.assertRaises(ProtocolError):
                outcome_metrics([{"p": p, "scores": {"public": value}}], self.weights)

    def test_invalid_budget_rejected(self):
        for budget in (True, -1, 9):
            packet = copy.deepcopy(self.packet)
            packet["budget"] = budget
            with self.assertRaises(ProtocolError):
                validate(packet)

    def test_bad_likelihood_rejected(self):
        self.packet["tests"][0]["positive_probability"].pop("ordinary")
        with self.assertRaises(ProtocolError):
            validate(self.packet)

    def test_uninformative_observation_preserves_belief(self):
        test = self.packet["tests"][0]
        test["positive_probability"] = {h: .5 for h in self.packet["prior"]}
        for positive in (True, False):
            self.assertEqual(update(self.packet["prior"], test, positive), self.packet["prior"])

    def test_no_information_means_stop_for_value_policies(self):
        for test in self.packet["tests"]:
            test["positive_probability"] = {h: .5 for h in self.packet["prior"]}
        for policy in ("myopic", "sequential", "entropy"):
            result = replay(self.packet, policy, lambda _: True)
            self.assertEqual(result["cost"], 0)
            self.assertEqual(result["history"], [])

    def test_excessive_investigation_cost_causes_stop(self):
        for test in self.packet["tests"]:
            test["cost"] = 10000
        self.assertIsNone(choose(self.packet, self.packet["prior"], method="sequential")["test_id"])

    def test_budget_and_family_are_enforced_for_all_policies(self):
        from syntruth.investigation import METHODS
        self.packet["budget"] = 1
        for method in METHODS:
            result = replay(self.packet, method, lambda _: True, seed=1)
            self.assertLessEqual(result["units"], 1)
        self.packet["budget"] = 3
        for test in self.packet["tests"]:
            test["family"] = "one_upstream_dataset"
        result = replay(self.packet, "fixed", lambda _: True)
        self.assertEqual(len(result["history"]), 1)

    def test_impossible_observation_is_reported(self):
        test = self.packet["tests"][0]
        test["positive_probability"] = {h: 0 for h in self.packet["prior"]}
        with self.assertRaises(ProtocolError):
            update(self.packet["prior"], test, True)

    def test_terminal_selects_feasible_alternative(self):
        self.packet["constraints"] = [{"stakeholder_id": "public", "floor": 0, "max_probability": 0}]
        action, _ = terminal(self.packet, self.packet["prior"])
        self.assertEqual(action, "baseline")

    def test_replay_is_deterministic_and_leaves_packet_unchanged(self):
        original = copy.deepcopy(self.packet)
        first = replay(self.packet, "random", lambda _: False, seed=2)
        self.assertEqual(first, replay(self.packet, "random", lambda _: False, seed=2))
        self.assertEqual(original, self.packet)

    def test_omitted_truth_never_enters_public_belief(self):
        truth, observations, _ = actual_case(self.packet, "omitted", 42)
        self.assertEqual(truth, "absent_mechanism")
        result = replay(self.packet, "sequential", observations.__getitem__)
        self.assertNotIn(truth, result["posterior"])

    def test_two_complementary_tests_have_value_when_each_alone_does_not(self):
        # Parity cannot be inferred from either bit alone, but both reveal it.
        hs = ["00", "01", "10", "11"]
        packet = {
            "protocol_version": "investigation-0.1", "title": "Complementary information",
            "hypotheses": [{"id": h} for h in hs], "prior": {h: .25 for h in hs},
            "stakeholder_weights": {"public": 1.0}, "baseline_action_id": "even",
            "budget": 2, "constraints": [], "actions": [], "tests": [],
        }
        for name, parity in (("even", 0), ("odd", 1)):
            packet["actions"].append({"id": name, "outcomes": {
                h: [{"p": 1, "scores": {"public": 10 if (int(h[0]) ^ int(h[1])) == parity else 0}}]
                for h in hs}})
        for bit in range(2):
            packet["tests"].append({"id": str(bit), "family": str(bit), "source": "fixture",
                                    "units": 1, "cost": 1,
                                    "positive_probability": {h: int(h[bit]) for h in hs}})
        validate(packet)
        self.assertIsNone(choose(packet, packet["prior"], method="myopic")["test_id"])
        choice = choose(packet, packet["prior"], method="sequential")
        self.assertIsNotNone(choice["test_id"])
        self.assertAlmostEqual(choice["candidate_values"][choice["test_id"]], 8)
        result = replay(packet, "sequential", lambda _: False)
        self.assertEqual(result["action_id"], "even")
        self.assertEqual(result["predicted_net_utility"], 8)


if __name__ == "__main__":
    unittest.main()

