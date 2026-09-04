from __future__ import annotations

import tempfile
import unittest

from syntruth.core import ProtocolError
from syntruth.provenance import (
    downstream_probability,
    pairwise_counts,
    recover_clusters,
    run_provenance_benchmark,
    validate_provenance_config,
    write_provenance_outputs,
)


def small_config() -> dict:
    return {
        "experiment_id": "test-provenance",
        "title": "Test provenance",
        "seed": 23,
        "bootstrap_seed": 24,
        "cases_per_cell": 8,
        "roots": [4],
        "max_family_size": [2],
        "citation_completeness": [0.0, 0.5, 0.9],
        "paraphrase_rate": [0.0, 0.4, 0.8],
        "topic_contamination": [0.1, 0.5],
        "signal_strength": 0.55,
        "report_noise_sd": 0.12,
        "lineage_tokens": 14,
        "topic_vocabulary_size": 24,
        "text_jaccard_threshold": 0.2,
        "bootstrap_samples": 50,
        "methods": ["oracle", "all_independent", "all_one", "citation", "text", "hybrid"],
    }


def documents() -> list[dict]:
    return [
        {
            "id": "a1",
            "family": "a",
            "tokens": {"alpha", "shared"},
            "observed_parent": None,
            "report": 0.4,
        },
        {
            "id": "a2",
            "family": "a",
            "tokens": {"alpha", "shared"},
            "observed_parent": "a1",
            "report": 0.5,
        },
        {
            "id": "b1",
            "family": "b",
            "tokens": {"beta", "shared"},
            "observed_parent": None,
            "report": -0.3,
        },
    ]


class ProvenanceTests(unittest.TestCase):
    def test_config_validation(self) -> None:
        validate_provenance_config(small_config())

    def test_unknown_method_rejected(self) -> None:
        config = small_config()
        config["methods"].append("telepathy")
        with self.assertRaises(ProtocolError):
            validate_provenance_config(config)

    def test_perfect_citation_recovers_families(self) -> None:
        items = documents()
        labels = recover_clusters(items, "citation", 0.2)
        counts = pairwise_counts(items, labels)
        self.assertEqual(counts, {"tp": 1, "fp": 0, "tn": 2, "fn": 0})

    def test_extreme_clusterings_score_as_expected(self) -> None:
        items = documents()
        independent = pairwise_counts(items, recover_clusters(items, "all_independent", 0.2))
        collapsed = pairwise_counts(items, recover_clusters(items, "all_one", 0.2))
        self.assertEqual(independent["fn"], 1)
        self.assertEqual(independent["fp"], 0)
        self.assertEqual(collapsed["tp"], 1)
        self.assertEqual(collapsed["fp"], 2)

    def test_downstream_probability_is_bounded(self) -> None:
        items = documents()
        labels = recover_clusters(items, "oracle", 0.2)
        probability = downstream_probability(items, labels, 0.55, 0.12)
        self.assertGreater(probability, 0.0)
        self.assertLess(probability, 1.0)

    def test_small_run_is_deterministic(self) -> None:
        first = run_provenance_benchmark(small_config())
        second = run_provenance_benchmark(small_config())
        self.assertEqual(first, second)

    def test_outputs_are_created(self) -> None:
        result = run_provenance_benchmark(small_config())
        with tempfile.TemporaryDirectory() as directory:
            paths = write_provenance_outputs(result, directory)
            self.assertTrue(all(path.exists() for path in paths.values()))


if __name__ == "__main__":
    unittest.main()
