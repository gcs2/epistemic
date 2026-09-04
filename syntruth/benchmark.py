"""Synthetic benchmarks for dependence-aware epistemic synthesis."""

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


METHODS = ("oracle", "estimated", "conservative", "naive", "one_per_group")
METRICS = ("brier", "log_loss", "accuracy", "ece", "confidently_wrong", "sharpness")


def load_benchmark_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    validate_benchmark_config(config)
    config["_config_path"] = str(config_path.resolve())
    config["_config_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    return config


def validate_benchmark_config(config: dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ProtocolError("Benchmark configuration must be an object")
    for field in ("experiment_id", "title"):
        if not isinstance(config.get(field), str) or not config[field].strip():
            raise ProtocolError(f"{field} must be a non-empty string")
    for field in ("seed", "bootstrap_seed", "trials_per_cell", "bootstrap_samples"):
        if not isinstance(config.get(field), int):
            raise ProtocolError(f"{field} must be an integer")
    if config["trials_per_cell"] <= 0 or config["bootstrap_samples"] < 0:
        raise ProtocolError("trials_per_cell must be positive and bootstrap_samples non-negative")
    for field in ("groups", "max_duplicates", "rho", "signal_strength"):
        if not isinstance(config.get(field), list) or not config[field]:
            raise ProtocolError(f"{field} must be a non-empty list")
    if any(not isinstance(value, int) or value <= 0 for value in config["groups"]):
        raise ProtocolError("groups values must be positive integers")
    if any(not isinstance(value, int) or value <= 0 for value in config["max_duplicates"]):
        raise ProtocolError("max_duplicates values must be positive integers")
    if any(not isinstance(value, (int, float)) or not 0 <= value <= 1 for value in config["rho"]):
        raise ProtocolError("rho values must be in [0, 1]")
    if any(not isinstance(value, (int, float)) or value <= 0 for value in config["signal_strength"]):
        raise ProtocolError("signal_strength values must be positive")
    for field in ("sigma", "rho_estimation_sd"):
        if not isinstance(config.get(field), (int, float)) or config[field] < 0:
            raise ProtocolError(f"{field} must be non-negative")
    if config["sigma"] == 0:
        raise ProtocolError("sigma must be positive")
    base_rate = config.get("base_rate")
    if not isinstance(base_rate, (int, float)) or not 0 < base_rate < 1:
        raise ProtocolError("base_rate must be in (0, 1)")
    methods = config.get("methods")
    if not isinstance(methods, list) or not methods or len(methods) != len(set(methods)):
        raise ProtocolError("methods must be a non-empty list of unique method ids")
    unknown = set(methods) - set(METHODS)
    if unknown:
        raise ProtocolError(f"Unknown methods: {', '.join(sorted(unknown))}")


def _sigmoid(value: float) -> float:
    if value >= 0:
        decay = math.exp(-value)
        return 1.0 / (1.0 + decay)
    growth = math.exp(value)
    return growth / (1.0 + growth)


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else float("nan")


def _mcse(values: list[float]) -> float:
    return statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0


def _ece(probabilities: list[float], outcomes: list[int], bins: int = 10) -> float:
    bucket_probabilities: list[list[float]] = [[] for _ in range(bins)]
    bucket_outcomes: list[list[int]] = [[] for _ in range(bins)]
    for probability, outcome in zip(probabilities, outcomes):
        index = min(bins - 1, int(probability * bins))
        bucket_probabilities[index].append(probability)
        bucket_outcomes[index].append(outcome)
    total = len(probabilities)
    return sum(
        (len(bucket) / total) * abs(_mean(bucket) - _mean(bucket_outcomes[index]))
        for index, bucket in enumerate(bucket_probabilities)
        if bucket
    )


def _method_probabilities(
    groups: list[tuple[list[float], float]],
    *,
    mu: float,
    sigma: float,
    prior_log_odds: float,
) -> dict[str, float]:
    multiplier = 2.0 * mu / (sigma * sigma)
    log_odds = {method: prior_log_odds for method in METHODS}
    for observations, rho_hat in groups:
        count = len(observations)
        total = sum(observations)
        true_rho = observations.true_rho if isinstance(observations, ObservationList) else 0.0
        log_odds["oracle"] += multiplier * total / (1.0 + (count - 1) * true_rho)
        log_odds["estimated"] += multiplier * total / (1.0 + (count - 1) * rho_hat)
        log_odds["conservative"] += multiplier * total / count
        log_odds["naive"] += multiplier * total
        log_odds["one_per_group"] += multiplier * observations[0]
    return {method: _sigmoid(value) for method, value in log_odds.items()}


class ObservationList(list[float]):
    """A list carrying the true within-group correlation for oracle evaluation."""

    def __init__(self, values: list[float], true_rho: float):
        super().__init__(values)
        self.true_rho = true_rho


def _summarize_predictions(probabilities: list[float], outcomes: list[int]) -> dict[str, float]:
    epsilon = 1e-15
    brier_values = [(probability - outcome) ** 2 for probability, outcome in zip(probabilities, outcomes)]
    log_values = [
        -(outcome * math.log(max(epsilon, probability)) + (1 - outcome) * math.log(max(epsilon, 1 - probability)))
        for probability, outcome in zip(probabilities, outcomes)
    ]
    accuracy_values = [float((probability >= 0.5) == bool(outcome)) for probability, outcome in zip(probabilities, outcomes)]
    confidently_wrong_values = [
        float((probability >= 0.9 and outcome == 0) or (probability <= 0.1 and outcome == 1))
        for probability, outcome in zip(probabilities, outcomes)
    ]
    return {
        "brier": _mean(brier_values),
        "brier_mcse": _mcse(brier_values),
        "log_loss": _mean(log_values),
        "log_loss_mcse": _mcse(log_values),
        "accuracy": _mean(accuracy_values),
        "ece": _ece(probabilities, outcomes),
        "confidently_wrong": _mean(confidently_wrong_values),
        "sharpness": _mean([abs(probability - 0.5) for probability in probabilities]),
    }


def _run_cell(
    config: dict[str, Any],
    rng: random.Random,
    *,
    group_count: int,
    max_duplicates: int,
    rho: float,
    mu: float,
) -> tuple[list[dict[str, Any]], float]:
    trials = int(config["trials_per_cell"])
    sigma = float(config["sigma"])
    base_rate = float(config["base_rate"])
    rho_estimation_sd = float(config["rho_estimation_sd"])
    prior_log_odds = math.log(base_rate / (1.0 - base_rate))
    methods = list(config["methods"])
    probabilities = {method: [] for method in methods}
    outcomes: list[int] = []
    maximum_spread = 0.0

    for _ in range(trials):
        outcome = int(rng.random() < base_rate)
        sign = 1.0 if outcome else -1.0
        evidence_groups: list[tuple[list[float], float]] = []
        for _group in range(group_count):
            count = rng.randint(1, max_duplicates)
            shared_error = rng.gauss(0.0, 1.0)
            observations = ObservationList(
                [
                    sign * mu
                    + sigma
                    * (
                        math.sqrt(rho) * shared_error
                        + math.sqrt(max(0.0, 1.0 - rho)) * rng.gauss(0.0, 1.0)
                    )
                    for _item in range(count)
                ],
                true_rho=rho,
            )
            rho_hat = min(0.999, max(0.0, rho + rng.gauss(0.0, rho_estimation_sd)))
            evidence_groups.append((observations, rho_hat))

        trial_probabilities = _method_probabilities(
            evidence_groups,
            mu=mu,
            sigma=sigma,
            prior_log_odds=prior_log_odds,
        )
        selected = [trial_probabilities[method] for method in methods]
        maximum_spread = max(maximum_spread, max(selected) - min(selected))
        for method in methods:
            probabilities[method].append(trial_probabilities[method])
        outcomes.append(outcome)

    rows: list[dict[str, Any]] = []
    for method in methods:
        row = {
            "groups": group_count,
            "max_duplicates": max_duplicates,
            "rho": rho,
            "signal_strength": mu,
            "trials": trials,
            "method": method,
        }
        row.update(_summarize_predictions(probabilities[method], outcomes))
        rows.append(row)
    return rows, maximum_spread


def _cell_key(row: dict[str, Any]) -> tuple[int, int, float, float]:
    return (
        int(row["groups"]),
        int(row["max_duplicates"]),
        float(row["rho"]),
        float(row["signal_strength"]),
    )


def _paired_differences(
    rows: list[dict[str, Any]], method_a: str, method_b: str, predicate=lambda row: True
) -> list[float]:
    lookup = {_cell_key(row) + (row["method"],): row for row in rows}
    cells = sorted({_cell_key(row) for row in rows if predicate(row)})
    return [
        float(lookup[cell + (method_a,)]["brier"]) - float(lookup[cell + (method_b,)]["brier"])
        for cell in cells
    ]


def _bootstrap_mean_interval(values: list[float], samples: int, seed: int) -> tuple[float, float]:
    if not values or samples == 0:
        mean = _mean(values)
        return mean, mean
    rng = random.Random(seed)
    means = [
        _mean([values[rng.randrange(len(values))] for _ in values])
        for _ in range(samples)
    ]
    means.sort()
    low = means[int(0.025 * (samples - 1))]
    high = means[int(0.975 * (samples - 1))]
    return low, high


def _average_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_method[row["method"]].append(row)
    result = []
    for method, method_rows in by_method.items():
        summary = {"method": method, "cells": len(method_rows)}
        for metric in METRICS:
            summary[metric] = _mean([float(row[metric]) for row in method_rows])
        result.append(summary)
    return sorted(result, key=lambda row: row["brier"])


def _naive_oracle_grid(rows: list[dict[str, Any]]) -> list[dict[str, float]]:
    lookup = {_cell_key(row) + (row["method"],): row for row in rows}
    grouped: dict[tuple[float, int], list[float]] = defaultdict(list)
    for cell in {_cell_key(row) for row in rows}:
        groups, duplicates, rho, mu = cell
        difference = lookup[cell + ("naive",)]["brier"] - lookup[cell + ("oracle",)]["brier"]
        grouped[(rho, duplicates)].append(float(difference))
    return [
        {"rho": rho, "max_duplicates": duplicates, "naive_minus_oracle_brier": _mean(values)}
        for (rho, duplicates), values in sorted(grouped.items())
    ]


def _nondecreasing(values: list[float], tolerance: float = 1e-5) -> bool:
    return all(current + tolerance >= previous for previous, current in zip(values, values[1:]))


def _evaluate_hypotheses(
    config: dict[str, Any], rows: list[dict[str, Any]], no_duplication_spread: float
) -> list[dict[str, Any]]:
    positive_duplicated = lambda row: float(row["rho"]) > 0 and int(row["max_duplicates"]) > 1
    high_dependence = lambda row: float(row["rho"]) >= 0.75 and int(row["max_duplicates"]) >= 4
    independent_duplicated = lambda row: float(row["rho"]) == 0 and int(row["max_duplicates"]) > 1

    naive_oracle = _paired_differences(rows, "naive", "oracle", positive_duplicated)
    ci_low, ci_high = _bootstrap_mean_interval(
        naive_oracle, int(config["bootstrap_samples"]), int(config["bootstrap_seed"])
    )

    high_conservative_naive = _paired_differences(rows, "conservative", "naive", high_dependence)
    independent_conservative_naive = _paired_differences(
        rows, "conservative", "naive", independent_duplicated
    )
    estimated_naive = _paired_differences(rows, "estimated", "naive", positive_duplicated)
    estimated_oracle = _paired_differences(rows, "estimated", "oracle", positive_duplicated)

    grid = _naive_oracle_grid(rows)
    by_rho: dict[float, list[float]] = defaultdict(list)
    by_duplicates: dict[int, list[float]] = defaultdict(list)
    for cell in grid:
        by_rho[float(cell["rho"])].append(float(cell["naive_minus_oracle_brier"]))
        by_duplicates[int(cell["max_duplicates"])].append(float(cell["naive_minus_oracle_brier"]))
    rho_sequence = [_mean(by_rho[key]) for key in sorted(by_rho)]
    duplicate_sequence = [_mean(by_duplicates[key]) for key in sorted(by_duplicates)]

    lookup = {_cell_key(row) + (row["method"],): row for row in rows}
    high_cells = sorted({_cell_key(row) for row in rows if high_dependence(row)})
    wrong_difference = _mean(
        [
            float(lookup[cell + ("conservative",)]["confidently_wrong"])
            - float(lookup[cell + ("naive",)]["confidently_wrong"])
            for cell in high_cells
        ]
    )

    return [
        {
            "id": "H1",
            "supported": _mean(naive_oracle) > 0 and ci_low > 0,
            "effect": _mean(naive_oracle),
            "detail": f"naive − oracle Brier = {_mean(naive_oracle):.6f}; bootstrap 95% interval [{ci_low:.6f}, {ci_high:.6f}]",
        },
        {
            "id": "H2",
            "supported": _nondecreasing(rho_sequence) and _nondecreasing(duplicate_sequence),
            "effect": rho_sequence[-1] - rho_sequence[0],
            "detail": "Averaged naive penalty is nondecreasing across registered rho and duplication grids.",
        },
        {
            "id": "H3",
            "supported": _mean(high_conservative_naive) < 0 and wrong_difference < 0,
            "effect": _mean(high_conservative_naive),
            "detail": f"high-dependence conservative − naive Brier = {_mean(high_conservative_naive):.6f}; confidently-wrong difference = {wrong_difference:.6f}",
        },
        {
            "id": "H4",
            "supported": _mean(independent_conservative_naive) > 0,
            "effect": _mean(independent_conservative_naive),
            "detail": f"rho=0 conservative − naive Brier = {_mean(independent_conservative_naive):.6f}",
        },
        {
            "id": "H5",
            "supported": _mean(estimated_naive) < 0 and _mean(estimated_oracle) > 0,
            "effect": _mean(estimated_naive),
            "detail": f"estimated − naive Brier = {_mean(estimated_naive):.6f}; estimated − oracle = {_mean(estimated_oracle):.6f}",
        },
        {
            "id": "H6",
            "supported": no_duplication_spread <= 1e-12,
            "effect": no_duplication_spread,
            "detail": f"maximum probability spread with one item per group = {no_duplication_spread:.3e}",
        },
    ]


def run_benchmark(config: dict[str, Any]) -> dict[str, Any]:
    validate_benchmark_config(config)
    rng = random.Random(int(config["seed"]))
    rows: list[dict[str, Any]] = []
    no_duplication_spread = 0.0
    grid = itertools.product(
        config["groups"],
        config["max_duplicates"],
        config["rho"],
        config["signal_strength"],
    )
    for group_count, max_duplicates, rho, mu in grid:
        cell_rows, spread = _run_cell(
            config,
            rng,
            group_count=int(group_count),
            max_duplicates=int(max_duplicates),
            rho=float(rho),
            mu=float(mu),
        )
        rows.extend(cell_rows)
        if int(max_duplicates) == 1:
            no_duplication_spread = max(no_duplication_spread, spread)

    result = {
        "experiment_id": config["experiment_id"],
        "title": config["title"],
        "config_sha256": config.get("_config_sha256"),
        "cells": len(rows) // len(config["methods"]),
        "trials": (len(rows) // len(config["methods"])) * int(config["trials_per_cell"]),
        "overall": _average_rows(rows),
        "hypotheses": _evaluate_hypotheses(config, rows, no_duplication_spread),
        "naive_oracle_grid": _naive_oracle_grid(rows),
        "rows": rows,
    }
    return result


def _format_method(method: str) -> str:
    return method.replace("_", " ").title()


def render_benchmark_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Confirmatory synthetic benchmark report. Interpret only within the preregistered data-generating mechanisms.",
        "",
        f"- **Cells:** {result['cells']:,}",
        f"- **Simulated trials:** {result['trials']:,}",
        f"- **Configuration SHA-256:** `{result.get('config_sha256') or 'not recorded'}`",
        "",
        "## Overall performance",
        "",
        "Lower Brier, log loss, calibration error, and confidently-wrong rate are better. Accuracy is higher-is-better. Cell means receive equal weight.",
        "",
        "| Method | Brier | Log loss | Accuracy | ECE | Confidently wrong | Sharpness |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["overall"]:
        lines.append(
            f"| {_format_method(row['method'])} | {row['brier']:.5f} | {row['log_loss']:.5f} | "
            f"{row['accuracy']:.1%} | {row['ece']:.4f} | {row['confidently_wrong']:.2%} | {row['sharpness']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Preregistered hypotheses",
            "",
            "| Hypothesis | Result | Registered effect |",
            "|---|---|---|",
        ]
    )
    for hypothesis in result["hypotheses"]:
        status = "Supported" if hypothesis["supported"] else "Not supported"
        lines.append(f"| {hypothesis['id']} | **{status}** | {hypothesis['detail']} |")

    rho_values = sorted({float(row["rho"]) for row in result["naive_oracle_grid"]})
    duplication_values = sorted({int(row["max_duplicates"]) for row in result["naive_oracle_grid"]})
    lookup = {
        (float(row["rho"]), int(row["max_duplicates"])): float(row["naive_minus_oracle_brier"])
        for row in result["naive_oracle_grid"]
    }
    lines.extend(
        [
            "",
            "## Dependence penalty surface",
            "",
            "Values are naive-independent Brier minus oracle Brier. Positive values mean naive synthesis is worse.",
            "",
            "| rho \\ max duplicates | " + " | ".join(str(value) for value in duplication_values) + " |",
            "|---:" + "|---:" * len(duplication_values) + "|",
        ]
    )
    for rho in rho_values:
        lines.append(
            f"| {rho:.2f} | "
            + " | ".join(f"{lookup[(rho, duplicates)]:.5f}" for duplicates in duplication_values)
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The oracle is advantaged by knowing the true correlation and is a reference bound. Conservative deduplication is intentionally cautious. Its comparison with naive synthesis reveals a real tradeoff: duplicate protection under high dependence versus lost information when grouped observations are independent.",
            "",
            "This experiment does not show that real-world dependence groups or correlations can be recovered reliably. That is the subject of later provenance-mapping and retrospective experiments.",
            "",
        ]
    )
    return "\n".join(lines)


def write_benchmark_outputs(result: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    report_path = directory / "report.md"
    summary_path = directory / "summary.json"
    cells_path = directory / "cells.csv"

    report_path.write_text(render_benchmark_markdown(result), encoding="utf-8")
    summary = {key: value for key, value in result.items() if key != "rows"}
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    fieldnames = list(result["rows"][0])
    with cells_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result["rows"])
    return {"report": report_path, "summary": summary_path, "cells": cells_path}
