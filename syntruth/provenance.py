"""Experiment 002A: recovery of hidden evidence families."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from .core import ProtocolError


METHODS = ("oracle", "all_independent", "all_one", "citation", "text", "hybrid")


def load_provenance_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    validate_provenance_config(config)
    config["_config_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    return config


def validate_provenance_config(config: dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ProtocolError("Provenance benchmark configuration must be an object")
    for field in ("experiment_id", "title"):
        if not isinstance(config.get(field), str) or not config[field].strip():
            raise ProtocolError(f"{field} must be a non-empty string")
    for field in ("seed", "bootstrap_seed", "cases_per_cell", "bootstrap_samples"):
        if not isinstance(config.get(field), int):
            raise ProtocolError(f"{field} must be an integer")
    if config["cases_per_cell"] <= 0 or config["bootstrap_samples"] < 0:
        raise ProtocolError("cases_per_cell must be positive and bootstrap_samples non-negative")
    for field in (
        "roots",
        "max_family_size",
        "citation_completeness",
        "paraphrase_rate",
        "topic_contamination",
    ):
        if not isinstance(config.get(field), list) or not config[field]:
            raise ProtocolError(f"{field} must be a non-empty list")
    if any(not isinstance(value, int) or value <= 0 for value in config["roots"]):
        raise ProtocolError("roots values must be positive integers")
    if any(not isinstance(value, int) or value <= 0 for value in config["max_family_size"]):
        raise ProtocolError("max_family_size values must be positive integers")
    for field in ("citation_completeness", "paraphrase_rate", "topic_contamination"):
        if any(not isinstance(value, (int, float)) or not 0 <= value <= 1 for value in config[field]):
            raise ProtocolError(f"{field} values must be in [0, 1]")
    for field in ("signal_strength", "report_noise_sd"):
        if not isinstance(config.get(field), (int, float)) or config[field] < 0:
            raise ProtocolError(f"{field} must be non-negative")
    for field in ("lineage_tokens", "topic_vocabulary_size"):
        if not isinstance(config.get(field), int) or config[field] <= 0:
            raise ProtocolError(f"{field} must be a positive integer")
    threshold = config.get("text_jaccard_threshold")
    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
        raise ProtocolError("text_jaccard_threshold must be in [0, 1]")
    methods = config.get("methods")
    if not isinstance(methods, list) or not methods or len(methods) != len(set(methods)):
        raise ProtocolError("methods must be a non-empty unique list")
    unknown = set(methods) - set(METHODS)
    if unknown:
        raise ProtocolError(f"Unknown provenance methods: {', '.join(sorted(unknown))}")


class UnionFind:
    def __init__(self, items: list[str]):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, first: str, second: str) -> None:
        root_a = self.find(first)
        root_b = self.find(second)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

    def labels(self) -> dict[str, str]:
        return {item: self.find(item) for item in self.parent}


def _jaccard(first: set[str], second: set[str]) -> float:
    union = first | second
    return len(first & second) / len(union) if union else 1.0


def _generate_case(
    config: dict[str, Any],
    rng: random.Random,
    *,
    roots: int,
    max_family_size: int,
    citation_completeness: float,
    paraphrase_rate: float,
    topic_contamination: float,
    case_number: int,
) -> tuple[int, list[dict[str, Any]]]:
    outcome = int(rng.random() < 0.5)
    sign = 1.0 if outcome else -1.0
    mu = float(config["signal_strength"])
    report_noise = float(config["report_noise_sd"])
    lineage_count = int(config["lineage_tokens"])
    topic_vocabulary = [f"topic_{index}" for index in range(int(config["topic_vocabulary_size"]))]
    documents: list[dict[str, Any]] = []

    for family in range(roots):
        family_size = rng.randint(1, max_family_size)
        root_signal = sign * mu + rng.gauss(0.0, 1.0)
        lineage = [f"case{case_number}_family{family}_fact{index}" for index in range(lineage_count)]
        family_documents: list[dict[str, Any]] = []
        for member in range(family_size):
            identifier = f"c{case_number}_f{family}_d{member}"
            tokens: set[str] = set()
            for token_index, token in enumerate(lineage):
                if member == 0 or rng.random() >= paraphrase_rate:
                    tokens.add(token)
                else:
                    tokens.add(f"alias_{identifier}_{token_index}")
            for topic in topic_vocabulary:
                if rng.random() < topic_contamination:
                    tokens.add(topic)
            parent = None
            observed_parent = None
            if member > 0:
                parent_document = family_documents[rng.randrange(member)]
                parent = parent_document["id"]
                if rng.random() < citation_completeness:
                    observed_parent = parent
            document = {
                "id": identifier,
                "family": f"family_{family}",
                "tokens": tokens,
                "parent": parent,
                "observed_parent": observed_parent,
                "report": root_signal + rng.gauss(0.0, report_noise),
            }
            documents.append(document)
            family_documents.append(document)
    return outcome, documents


def recover_clusters(
    documents: list[dict[str, Any]], method: str, text_threshold: float
) -> dict[str, str]:
    identifiers = [document["id"] for document in documents]
    if method == "oracle":
        return {document["id"]: document["family"] for document in documents}
    if method == "all_independent":
        return {identifier: identifier for identifier in identifiers}
    if method == "all_one":
        return {identifier: "all" for identifier in identifiers}
    if method not in {"citation", "text", "hybrid"}:
        raise ProtocolError(f"Unknown recovery method: {method}")

    union_find = UnionFind(identifiers)
    if method in {"citation", "hybrid"}:
        for document in documents:
            if document["observed_parent"] is not None:
                union_find.union(document["id"], document["observed_parent"])
    if method in {"text", "hybrid"}:
        for first_index, first in enumerate(documents):
            for second in documents[first_index + 1 :]:
                if _jaccard(first["tokens"], second["tokens"]) >= text_threshold:
                    union_find.union(first["id"], second["id"])
    return union_find.labels()


def pairwise_counts(
    documents: list[dict[str, Any]], predicted: dict[str, str]
) -> dict[str, int]:
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for first_index, first in enumerate(documents):
        for second in documents[first_index + 1 :]:
            true_same = first["family"] == second["family"]
            predicted_same = predicted[first["id"]] == predicted[second["id"]]
            if true_same and predicted_same:
                counts["tp"] += 1
            elif not true_same and predicted_same:
                counts["fp"] += 1
            elif true_same and not predicted_same:
                counts["fn"] += 1
            else:
                counts["tn"] += 1
    return counts


def _safe_ratio(numerator: float, denominator: float, empty_value: float = 0.0) -> float:
    return numerator / denominator if denominator else empty_value


def _structural_metrics(counts: dict[str, int]) -> dict[str, float]:
    precision = _safe_ratio(counts["tp"], counts["tp"] + counts["fp"], 1.0)
    recall = _safe_ratio(counts["tp"], counts["tp"] + counts["fn"], 1.0)
    f1 = _safe_ratio(2 * precision * recall, precision + recall)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_independence": _safe_ratio(counts["fn"], counts["tp"] + counts["fn"]),
        "false_dependence": _safe_ratio(counts["fp"], counts["tn"] + counts["fp"]),
    }


def _sigmoid(value: float) -> float:
    if value >= 0:
        decay = math.exp(-value)
        return 1.0 / (1.0 + decay)
    growth = math.exp(value)
    return growth / (1.0 + growth)


def downstream_probability(
    documents: list[dict[str, Any]], labels: dict[str, str], mu: float, report_noise_sd: float
) -> float:
    clusters: dict[str, list[float]] = defaultdict(list)
    for document in documents:
        clusters[labels[document["id"]]].append(float(document["report"]))
    log_odds = 0.0
    for reports in clusters.values():
        variance = 1.0 + report_noise_sd * report_noise_sd / len(reports)
        log_odds += 2.0 * mu * statistics.fmean(reports) / variance
    return _sigmoid(log_odds)


def _probability_metrics(probabilities: list[float], outcomes: list[int]) -> dict[str, float]:
    epsilon = 1e-15
    brier = [(probability - outcome) ** 2 for probability, outcome in zip(probabilities, outcomes)]
    log_loss = [
        -(outcome * math.log(max(epsilon, probability)) + (1 - outcome) * math.log(max(epsilon, 1 - probability)))
        for probability, outcome in zip(probabilities, outcomes)
    ]
    return {
        "brier": statistics.fmean(brier),
        "brier_mcse": statistics.stdev(brier) / math.sqrt(len(brier)) if len(brier) > 1 else 0.0,
        "log_loss": statistics.fmean(log_loss),
        "accuracy": statistics.fmean(
            float((probability >= 0.5) == bool(outcome))
            for probability, outcome in zip(probabilities, outcomes)
        ),
        "confidently_wrong": statistics.fmean(
            float((probability >= 0.9 and outcome == 0) or (probability <= 0.1 and outcome == 1))
            for probability, outcome in zip(probabilities, outcomes)
        ),
        "sharpness": statistics.fmean(abs(probability - 0.5) for probability in probabilities),
    }


def _run_cell(
    config: dict[str, Any],
    rng: random.Random,
    *,
    roots: int,
    max_family_size: int,
    citation_completeness: float,
    paraphrase_rate: float,
    topic_contamination: float,
    case_offset: int,
) -> list[dict[str, Any]]:
    methods = list(config["methods"])
    accumulated_counts = {method: {"tp": 0, "fp": 0, "tn": 0, "fn": 0} for method in methods}
    source_count_errors = {method: [] for method in methods}
    probabilities = {method: [] for method in methods}
    outcomes: list[int] = []
    for local_case in range(int(config["cases_per_cell"])):
        outcome, documents = _generate_case(
            config,
            rng,
            roots=roots,
            max_family_size=max_family_size,
            citation_completeness=citation_completeness,
            paraphrase_rate=paraphrase_rate,
            topic_contamination=topic_contamination,
            case_number=case_offset + local_case,
        )
        for method in methods:
            labels = recover_clusters(documents, method, float(config["text_jaccard_threshold"]))
            counts = pairwise_counts(documents, labels)
            for key in accumulated_counts[method]:
                accumulated_counts[method][key] += counts[key]
            predicted_count = len(set(labels.values()))
            source_count_errors[method].append(abs(predicted_count - roots) / roots)
            probabilities[method].append(
                downstream_probability(
                    documents,
                    labels,
                    float(config["signal_strength"]),
                    float(config["report_noise_sd"]),
                )
            )
        outcomes.append(outcome)

    rows: list[dict[str, Any]] = []
    for method in methods:
        row = {
            "roots": roots,
            "max_family_size": max_family_size,
            "citation_completeness": citation_completeness,
            "paraphrase_rate": paraphrase_rate,
            "topic_contamination": topic_contamination,
            "cases": int(config["cases_per_cell"]),
            "method": method,
            **accumulated_counts[method],
            **_structural_metrics(accumulated_counts[method]),
            "source_count_error": statistics.fmean(source_count_errors[method]),
            **_probability_metrics(probabilities[method], outcomes),
        }
        rows.append(row)
    return rows


def _cell_key(row: dict[str, Any]) -> tuple[int, int, float, float, float]:
    return (
        int(row["roots"]),
        int(row["max_family_size"]),
        float(row["citation_completeness"]),
        float(row["paraphrase_rate"]),
        float(row["topic_contamination"]),
    )


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else float("nan")


def _overall(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)
    metrics = (
        "precision",
        "recall",
        "f1",
        "false_independence",
        "false_dependence",
        "source_count_error",
        "brier",
        "log_loss",
        "accuracy",
        "confidently_wrong",
        "sharpness",
    )
    result = []
    for method, method_rows in grouped.items():
        result.append(
            {
                "method": method,
                "cells": len(method_rows),
                **{metric: _mean([float(row[metric]) for row in method_rows]) for metric in metrics},
            }
        )
    return sorted(result, key=lambda row: row["brier"])


def _paired_brier(
    rows: list[dict[str, Any]], first: str, second: str, predicate=lambda row: True
) -> list[float]:
    lookup = {_cell_key(row) + (row["method"],): row for row in rows}
    cells = sorted({_cell_key(row) for row in rows if predicate(row)})
    return [
        float(lookup[cell + (first,)]["brier"]) - float(lookup[cell + (second,)]["brier"])
        for cell in cells
    ]


def _bootstrap_interval(values: list[float], samples: int, seed: int) -> tuple[float, float]:
    if not values or samples == 0:
        mean = _mean(values)
        return mean, mean
    rng = random.Random(seed)
    estimates = [
        _mean([values[rng.randrange(len(values))] for _ in values])
        for _ in range(samples)
    ]
    estimates.sort()
    return estimates[int(0.025 * (samples - 1))], estimates[int(0.975 * (samples - 1))]


def _stratum_mean(rows: list[dict[str, Any]], method: str, metric: str, predicate) -> float:
    return _mean([float(row[metric]) for row in rows if row["method"] == method and predicate(row)])


def _evaluate_hypotheses(config: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citation_precision = _stratum_mean(rows, "citation", "precision", lambda row: True)
    citation_recalls = {
        level: _stratum_mean(
            rows, "citation", "recall", lambda row, level=level: float(row["citation_completeness"]) == level
        )
        for level in (0.0, 0.5, 0.9)
    }
    text_recalls = {
        level: _stratum_mean(rows, "text", "recall", lambda row, level=level: float(row["paraphrase_rate"]) == level)
        for level in (0.0, 0.4, 0.8)
    }
    text_false_dependence = {
        level: _stratum_mean(
            rows, "text", "false_dependence", lambda row, level=level: float(row["topic_contamination"]) == level
        )
        for level in (0.1, 0.5)
    }
    hybrid_recall = _stratum_mean(rows, "hybrid", "recall", lambda row: True)
    citation_recall = _stratum_mean(rows, "citation", "recall", lambda row: True)
    text_recall = _stratum_mean(rows, "text", "recall", lambda row: True)
    hybrid_precision = _stratum_mean(rows, "hybrid", "precision", lambda row: True)

    recoverable = lambda row: float(row["citation_completeness"]) >= 0.5 and float(row["paraphrase_rate"]) <= 0.4
    hybrid_naive = _paired_brier(rows, "hybrid", "all_independent", recoverable)
    hybrid_oracle = _paired_brier(rows, "hybrid", "oracle", lambda row: int(row["max_family_size"]) > 1)
    all_one_oracle = _paired_brier(rows, "all_one", "oracle", lambda row: int(row["roots"]) >= 4)
    hybrid_naive_ci = _bootstrap_interval(
        hybrid_naive, int(config["bootstrap_samples"]), int(config["bootstrap_seed"])
    )
    hybrid_oracle_ci = _bootstrap_interval(
        hybrid_oracle, int(config["bootstrap_samples"]), int(config["bootstrap_seed"]) + 1
    )
    all_one_oracle_ci = _bootstrap_interval(
        all_one_oracle, int(config["bootstrap_samples"]), int(config["bootstrap_seed"]) + 2
    )

    return [
        {
            "id": "H1",
            "supported": citation_precision >= 0.98,
            "effect": citation_precision,
            "detail": f"citation aggregate precision = {citation_precision:.4f}",
        },
        {
            "id": "H2",
            "supported": citation_recalls[0.9] > citation_recalls[0.5] > citation_recalls[0.0],
            "effect": citation_recalls[0.9] - citation_recalls[0.0],
            "detail": "citation recall at completeness 0/0.5/0.9 = "
            + "/".join(f"{citation_recalls[level]:.4f}" for level in (0.0, 0.5, 0.9)),
        },
        {
            "id": "H3",
            "supported": text_recalls[0.0] > text_recalls[0.4] > text_recalls[0.8],
            "effect": text_recalls[0.0] - text_recalls[0.8],
            "detail": "text recall at paraphrase 0/0.4/0.8 = "
            + "/".join(f"{text_recalls[level]:.4f}" for level in (0.0, 0.4, 0.8)),
        },
        {
            "id": "H4",
            "supported": text_false_dependence[0.5] > text_false_dependence[0.1],
            "effect": text_false_dependence[0.5] - text_false_dependence[0.1],
            "detail": "text false-dependence at contamination 0.1/0.5 = "
            + "/".join(f"{text_false_dependence[level]:.4f}" for level in (0.1, 0.5)),
        },
        {
            "id": "H5",
            "supported": hybrid_recall > citation_recall and hybrid_recall > text_recall and hybrid_precision >= 0.90,
            "effect": hybrid_recall - max(citation_recall, text_recall),
            "detail": f"recall hybrid/citation/text = {hybrid_recall:.4f}/{citation_recall:.4f}/{text_recall:.4f}; hybrid precision = {hybrid_precision:.4f}",
        },
        {
            "id": "H6",
            "supported": _mean(hybrid_naive) < 0 and hybrid_naive_ci[1] < 0,
            "effect": _mean(hybrid_naive),
            "detail": f"recoverable hybrid − all-independent Brier = {_mean(hybrid_naive):.6f}; 95% interval [{hybrid_naive_ci[0]:.6f}, {hybrid_naive_ci[1]:.6f}]",
        },
        {
            "id": "H7",
            "supported": _mean(hybrid_oracle) > 0 and hybrid_oracle_ci[0] > 0,
            "effect": _mean(hybrid_oracle),
            "detail": f"nontrivial hybrid − oracle Brier = {_mean(hybrid_oracle):.6f}; 95% interval [{hybrid_oracle_ci[0]:.6f}, {hybrid_oracle_ci[1]:.6f}]",
        },
        {
            "id": "H8",
            "supported": _mean(all_one_oracle) > 0 and all_one_oracle_ci[0] > 0,
            "effect": _mean(all_one_oracle),
            "detail": f"all-one − oracle Brier = {_mean(all_one_oracle):.6f}; 95% interval [{all_one_oracle_ci[0]:.6f}, {all_one_oracle_ci[1]:.6f}]",
        },
    ]


def run_provenance_benchmark(config: dict[str, Any]) -> dict[str, Any]:
    validate_provenance_config(config)
    rng = random.Random(int(config["seed"]))
    rows: list[dict[str, Any]] = []
    case_offset = 0
    grid = itertools.product(
        config["roots"],
        config["max_family_size"],
        config["citation_completeness"],
        config["paraphrase_rate"],
        config["topic_contamination"],
    )
    for roots, max_family_size, citation, paraphrase, contamination in grid:
        rows.extend(
            _run_cell(
                config,
                rng,
                roots=int(roots),
                max_family_size=int(max_family_size),
                citation_completeness=float(citation),
                paraphrase_rate=float(paraphrase),
                topic_contamination=float(contamination),
                case_offset=case_offset,
            )
        )
        case_offset += int(config["cases_per_cell"])
    return {
        "experiment_id": config["experiment_id"],
        "title": config["title"],
        "config_sha256": config.get("_config_sha256"),
        "cells": len(rows) // len(config["methods"]),
        "cases": (len(rows) // len(config["methods"])) * int(config["cases_per_cell"]),
        "overall": _overall(rows),
        "hypotheses": _evaluate_hypotheses(config, rows),
        "rows": rows,
    }


def _method_label(method: str) -> str:
    return method.replace("_", " ").title()


def render_provenance_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Confirmatory synthetic-pilot report. Structural recovery is evaluated against hidden generated ancestry.",
        "",
        f"- **Cells:** {result['cells']:,}",
        f"- **Generated cases:** {result['cases']:,}",
        f"- **Configuration SHA-256:** `{result.get('config_sha256') or 'not recorded'}`",
        "",
        "## Overall provenance recovery",
        "",
        "| Method | Precision | Recall | F1 | False independence | False dependence | Source-count error |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    by_method = {row["method"]: row for row in result["overall"]}
    for method in ("oracle", "all_independent", "all_one", "citation", "text", "hybrid"):
        row = by_method[method]
        lines.append(
            f"| {_method_label(method)} | {row['precision']:.1%} | {row['recall']:.1%} | {row['f1']:.1%} | "
            f"{row['false_independence']:.1%} | {row['false_dependence']:.1%} | {row['source_count_error']:.1%} |"
        )
    lines.extend(
        [
            "",
            "## Downstream truth estimation",
            "",
            "| Method | Brier | Log loss | Accuracy | Confidently wrong | Sharpness |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in result["overall"]:
        lines.append(
            f"| {_method_label(row['method'])} | {row['brier']:.5f} | {row['log_loss']:.5f} | "
            f"{row['accuracy']:.1%} | {row['confidently_wrong']:.2%} | {row['sharpness']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Preregistered hypotheses",
            "",
            "| Hypothesis | Result | Registered contrast |",
            "|---|---|---|",
        ]
    )
    for hypothesis in result["hypotheses"]:
        status = "Supported" if hypothesis["supported"] else "Not supported"
        lines.append(f"| {hypothesis['id']} | **{status}** | {hypothesis['detail']} |")
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This pilot asks whether observable inheritance signals can recover a known hidden graph. It does not establish performance on natural prose, multi-parent claims, false citations, strategic source laundering, or real human and agent workflows.",
            "",
        ]
    )
    return "\n".join(lines)


def write_provenance_outputs(result: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    report_path = directory / "report.md"
    summary_path = directory / "summary.json"
    cells_path = directory / "cells.csv"
    report_path.write_text(render_provenance_markdown(result), encoding="utf-8")
    summary_path.write_text(
        json.dumps({key: value for key, value in result.items() if key != "rows"}, indent=2),
        encoding="utf-8",
    )
    with cells_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    return {"report": report_path, "summary": summary_path, "cells": cells_path}
