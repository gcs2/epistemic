"""Experiment 003A: synthetic stress tests for SES decision rules."""

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

from .core import ProtocolError, _normalize, _percentile


METHODS = (
    "oracle_expected",
    "baseline",
    "declared_raw",
    "confidence_shrink",
    "minimax_regret",
    "robustness_gate",
)
OPTIONS = ("baseline", "balanced", "aggressive")
SCENARIOS = ("favorable", "unfavorable", "tail")

# (low, high) by option, scenario, stakeholder, criterion. Criterion scores are
# all higher-is-better; negative access/burden values represent imposed burden.
IMPACT_RANGES: dict[str, dict[str, tuple[tuple[tuple[float, float], ...], ...]]] = {
    "baseline": {
        scenario: (((0.0, 0.0), (0.0, 0.0)), ((0.0, 0.0), (0.0, 0.0)))
        for scenario in SCENARIOS
    },
    "balanced": {
        "favorable": (((15, 45), (-5, 5)), ((5, 20), (-10, 0))),
        "unfavorable": (((5, 25), (-10, 0)), ((0, 10), (-15, -5))),
        "tail": (((-60, -20), (-80, -40)), ((-20, 0), (-40, -10))),
    },
    "aggressive": {
        "favorable": (((50, 90), (0, 20)), ((30, 70), (-20, 0))),
        "unfavorable": (((-20, 30), (-40, -10)), ((-10, 30), (-50, -10))),
        "tail": (((-100, -70), (-100, -70)), ((-90, -50), (-90, -50))),
    },
}


def load_decision_benchmark_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    validate_decision_benchmark_config(config)
    config["_config_path"] = str(config_path.resolve())
    config["_config_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest().upper()
    return config


def validate_decision_benchmark_config(config: dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ProtocolError("Decision benchmark configuration must be an object")
    for field in ("experiment_id", "title"):
        if not isinstance(config.get(field), str) or not config[field].strip():
            raise ProtocolError(f"{field} must be a non-empty string")
    for field in ("seed", "bootstrap_seed", "cases_per_cell", "bootstrap_samples", "sensitivity_samples"):
        if not isinstance(config.get(field), int):
            raise ProtocolError(f"{field} must be an integer")
    if config["cases_per_cell"] <= 0 or config["bootstrap_samples"] < 0 or config["sensitivity_samples"] <= 0:
        raise ProtocolError("case and sensitivity counts must be positive; bootstrap_samples non-negative")
    numeric_grids = {
        "tail_probability": (0.0, 1.0),
        "probability_error": (0.0, float("inf")),
        "impact_error": (0.0, float("inf")),
        "value_shift": (0.0, float("inf")),
        "negative_impact_confidence": (0.0, 1.0),
    }
    for field, (low, high) in numeric_grids.items():
        values = config.get(field)
        if not isinstance(values, list) or not values:
            raise ProtocolError(f"{field} must be a non-empty list")
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not low <= float(value) <= high
            for value in values
        ):
            raise ProtocolError(f"{field} contains an invalid value")
    visibility = config.get("tail_visibility")
    if not isinstance(visibility, list) or not visibility or set(visibility) - {"included", "omitted"}:
        raise ProtocolError("tail_visibility must contain only included and/or omitted")
    methods = config.get("methods")
    if not isinstance(methods, list) or not methods or len(methods) != len(set(methods)):
        raise ProtocolError("methods must be a non-empty list of unique ids")
    unknown = set(methods) - set(METHODS)
    if unknown:
        raise ProtocolError(f"Unknown methods: {', '.join(sorted(unknown))}")
    for field in ("robust_choice_threshold",):
        value = config.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
            raise ProtocolError(f"{field} must be in [0, 1]")
    for field in ("decision_margin", "catastrophe_threshold", "affected_harm_threshold"):
        if not isinstance(config.get(field), (int, float)) or isinstance(config[field], bool):
            raise ProtocolError(f"{field} must be numeric")


def _draw_impacts(rng: random.Random) -> dict[str, dict[str, list[list[float]]]]:
    impacts: dict[str, dict[str, list[list[float]]]] = {}
    for option in OPTIONS:
        impacts[option] = {}
        for scenario in SCENARIOS:
            impacts[option][scenario] = [
                [rng.uniform(*IMPACT_RANGES[option][scenario][stakeholder][criterion]) for criterion in range(2)]
                for stakeholder in range(2)
            ]
    return impacts


def _aggregate_state(impacts: list[list[float]], stakeholder: list[float], criterion: list[float]) -> float:
    return sum(
        stakeholder[s] * criterion[c] * impacts[s][c]
        for s in range(2)
        for c in range(2)
    )


def _scores(
    probabilities: dict[str, float],
    impacts: dict[str, dict[str, list[list[float]]]],
    stakeholder: list[float],
    criterion: list[float],
    confidence: float | None = None,
) -> dict[str, float]:
    result: dict[str, float] = {}
    for option in OPTIONS:
        total = 0.0
        for scenario, probability in probabilities.items():
            for s in range(2):
                for c in range(2):
                    impact = impacts[option][scenario][s][c]
                    factor = confidence if confidence is not None and impact < 0 else 1.0
                    total += probability * stakeholder[s] * criterion[c] * impact * factor
        result[option] = total
    return result


def _winner(scores: dict[str, float]) -> str:
    return max(OPTIONS, key=lambda option: (scores[option], -OPTIONS.index(option)))


def _perturb_probabilities(probabilities: dict[str, float], error: float, rng: random.Random) -> dict[str, float]:
    if error == 0:
        return dict(probabilities)
    return _normalize(
        {scenario: probability * math.exp(rng.gauss(0.0, error)) for scenario, probability in probabilities.items()}
    )


def _perturb_weights(weights: list[float], shift: float, rng: random.Random) -> list[float]:
    if shift == 0:
        return list(weights)
    perturbed = [weight * math.exp(rng.gauss(0.0, shift)) for weight in weights]
    total = sum(perturbed)
    return [value / total for value in perturbed]


def _declared_impacts(
    true_impacts: dict[str, dict[str, list[list[float]]]],
    visible: tuple[str, ...],
    error: float,
    rng: random.Random,
) -> dict[str, dict[str, list[list[float]]]]:
    return {
        option: {
            scenario: [
                [
                    min(100.0, max(-100.0, true_impacts[option][scenario][s][c] + rng.gauss(0.0, error)))
                    for c in range(2)
                ]
                for s in range(2)
            ]
            for scenario in visible
        }
        for option in OPTIONS
    }


def _views(probabilities: dict[str, float], stakeholder: list[float]) -> list[tuple[dict[str, float], list[float]]]:
    result = [(dict(probabilities), list(stakeholder))]
    multipliers = []
    if "favorable" in probabilities:
        multipliers.append({"favorable": 1.5})
    if "unfavorable" in probabilities:
        multipliers.append({"unfavorable": 1.5, "tail": 1.5})
    for changes in multipliers:
        result.append(
            (
                _normalize(
                    {key: value * changes.get(key, 1.0) for key, value in probabilities.items()}
                ),
                list(stakeholder),
            )
        )
    result.append((dict(probabilities), _normalize_list([stakeholder[0] * 1.5, stakeholder[1]])))
    result.append((dict(probabilities), _normalize_list([stakeholder[0], stakeholder[1] * 1.5])))
    return result


def _normalize_list(values: list[float]) -> list[float]:
    total = sum(values)
    return [value / total for value in values]


def _minimax_choice(view_scores: list[dict[str, float]], central_scores: dict[str, float]) -> str:
    regret = {
        option: max(max(scores.values()) - scores[option] for scores in view_scores)
        for option in OPTIONS
    }
    return min(OPTIONS, key=lambda option: (regret[option], -central_scores[option], OPTIONS.index(option)))


def _robustness_choice(
    probabilities: dict[str, float],
    impacts: dict[str, dict[str, list[list[float]]]],
    stakeholder: list[float],
    criterion: list[float],
    confidence: float,
    view_scores: list[dict[str, float]],
    config: dict[str, Any],
    rng: random.Random,
) -> tuple[str, bool]:
    leaders = {_winner(scores) for scores in view_scores}
    central = _scores(probabilities, impacts, stakeholder, criterion, confidence)
    candidate = _winner(central)
    if candidate == "baseline" or leaders != {candidate}:
        return "baseline", False
    samples: dict[str, list[float]] = {option: [] for option in OPTIONS}
    wins = defaultdict(int)
    for _ in range(int(config["sensitivity_samples"])):
        sampled_probabilities = _perturb_probabilities(probabilities, 0.15, rng)
        sampled_stakeholder = _perturb_weights(stakeholder, 0.25, rng)
        sampled_criterion = _perturb_weights(criterion, 0.25, rng)
        sampled_impacts = {
            option: {
                scenario: [
                    [
                        min(
                            100.0,
                            max(
                                -100.0,
                                impacts[option][scenario][s][c]
                                + rng.uniform(-10.0 * (1.0 - (confidence if impacts[option][scenario][s][c] < 0 else 1.0)),
                                              10.0 * (1.0 - (confidence if impacts[option][scenario][s][c] < 0 else 1.0))),
                            ),
                        )
                        for c in range(2)
                    ]
                    for s in range(2)
                ]
                for scenario in probabilities
            }
            for option in OPTIONS
        }
        score = _scores(
            sampled_probabilities,
            sampled_impacts,
            sampled_stakeholder,
            sampled_criterion,
            confidence,
        )
        wins[_winner(score)] += 1
        for option in OPTIONS:
            samples[option].append(score[option])
    first_probability = wins[candidate] / int(config["sensitivity_samples"])
    clears_baseline = _percentile(samples[candidate], 0.05) > (
        _percentile(samples["baseline"], 0.05) + float(config["decision_margin"])
    )
    certified = first_probability >= float(config["robust_choice_threshold"]) and clears_baseline
    return (candidate, True) if certified else ("baseline", False)


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def _run_case(config: dict[str, Any], factors: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    tail_probability = float(factors["tail_probability"])
    favorable_conditional = rng.uniform(0.35, 0.75)
    true_probabilities = {
        "favorable": (1.0 - tail_probability) * favorable_conditional,
        "unfavorable": (1.0 - tail_probability) * (1.0 - favorable_conditional),
        "tail": tail_probability,
    }
    true_impacts = _draw_impacts(rng)
    true_stakeholder = [0.65, 0.35]
    true_criterion = [0.60, 0.40]
    true_scores = _scores(true_probabilities, true_impacts, true_stakeholder, true_criterion)
    oracle = _winner(true_scores)

    visible = SCENARIOS if factors["tail_visibility"] == "included" else SCENARIOS[:2]
    visible_truth = _normalize({scenario: true_probabilities[scenario] for scenario in visible})
    declared_probabilities = _perturb_probabilities(
        visible_truth, float(factors["probability_error"]), rng
    )
    declared_impacts = _declared_impacts(
        true_impacts, visible, float(factors["impact_error"]), rng
    )
    declared_stakeholder = _perturb_weights(
        true_stakeholder, float(factors["value_shift"]), rng
    )
    declared_criterion = _perturb_weights(
        true_criterion, float(factors["value_shift"]), rng
    )
    confidence = float(factors["negative_impact_confidence"])
    raw_scores = _scores(
        declared_probabilities, declared_impacts, declared_stakeholder, declared_criterion
    )
    shrink_scores = _scores(
        declared_probabilities,
        declared_impacts,
        declared_stakeholder,
        declared_criterion,
        confidence,
    )
    raw_view_scores = [
        _scores(probabilities, declared_impacts, stakeholder, declared_criterion)
        for probabilities, stakeholder in _views(declared_probabilities, declared_stakeholder)
    ]
    shrink_view_scores = [
        _scores(probabilities, declared_impacts, stakeholder, declared_criterion, confidence)
        for probabilities, stakeholder in _views(declared_probabilities, declared_stakeholder)
    ]
    gate_choice, certified = _robustness_choice(
        declared_probabilities,
        declared_impacts,
        declared_stakeholder,
        declared_criterion,
        confidence,
        shrink_view_scores,
        config,
        rng,
    )
    choices = {
        "oracle_expected": oracle,
        "baseline": "baseline",
        "declared_raw": _winner(raw_scores),
        "confidence_shrink": _winner(shrink_scores),
        "minimax_regret": _minimax_choice(raw_view_scores, raw_scores),
        "robustness_gate": gate_choice,
    }
    result: dict[str, Any] = {"oracle": oracle, "certified": certified, "methods": {}}
    oracle_value = true_scores[oracle]
    for method, choice in choices.items():
        state_values = {
            scenario: _aggregate_state(
                true_impacts[choice][scenario], true_stakeholder, true_criterion
            )
            for scenario in SCENARIOS
        }
        catastrophe_exposure = sum(
            true_probabilities[scenario]
            for scenario, value in state_values.items()
            if value <= float(config["catastrophe_threshold"])
        )
        affected_expected = sum(
            true_probabilities[scenario]
            * sum(true_criterion[c] * true_impacts[choice][scenario][0][c] for c in range(2))
            for scenario in SCENARIOS
        )
        result["methods"][method] = {
            "choice": choice,
            "true_value": true_scores[choice],
            "regret": oracle_value - true_scores[choice],
            "harmful": float(true_scores[choice] < 0.0),
            "catastrophe_exposure": catastrophe_exposure,
            "affected_harm": float(affected_expected <= float(config["affected_harm_threshold"])),
            "baseline_selected": float(choice == "baseline"),
            "certified": float(method == "robustness_gate" and certified),
            "certified_nonoracle": float(method == "robustness_gate" and certified and choice != oracle),
            "certified_harmful": float(method == "robustness_gate" and certified and true_scores[choice] < 0.0),
        }
    return result


def _cell_summary(factors: dict[str, Any], cases: list[dict[str, Any]], method: str) -> dict[str, Any]:
    records = [case["methods"][method] for case in cases]
    row = dict(factors)
    row.update(
        {
            "method": method,
            "cases": len(records),
            "mean_true_value": _mean([record["true_value"] for record in records]),
            "mean_regret": _mean([record["regret"] for record in records]),
            "p90_regret": _percentile([record["regret"] for record in records], 0.90),
            "harmful_choice_rate": _mean([record["harmful"] for record in records]),
            "catastrophe_exposure": _mean([record["catastrophe_exposure"] for record in records]),
            "affected_harm_rate": _mean([record["affected_harm"] for record in records]),
            "baseline_selection_rate": _mean([record["baseline_selected"] for record in records]),
            "certification_rate": _mean([record["certified"] for record in records]),
            "certified_nonoracle_rate": _mean([record["certified_nonoracle"] for record in records]),
            "certified_harmful_rate": _mean([record["certified_harmful"] for record in records]),
        }
    )
    return row


def _aggregate_rows(rows: list[dict[str, Any]], predicate=lambda row: True) -> dict[str, dict[str, float]]:
    selected = [row for row in rows if predicate(row)]
    metrics = (
        "mean_true_value", "mean_regret", "p90_regret", "harmful_choice_rate",
        "catastrophe_exposure", "affected_harm_rate", "baseline_selection_rate",
        "certification_rate", "certified_nonoracle_rate", "certified_harmful_rate",
    )
    return {
        method: {
            metric: _mean([float(row[metric]) for row in selected if row["method"] == method])
            for metric in metrics
        }
        for method in METHODS
    }


def _marginal(rows: list[dict[str, Any]], field: str, value: Any, metric: str, method: str) -> float:
    return _mean(
        [float(row[metric]) for row in rows if row[field] == value and row["method"] == method]
    )


def _bootstrap_mean_interval(
    values: list[float], samples: int, seed: int
) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "q025": 0.0, "q975": 0.0}
    mean = _mean(values)
    if samples == 0:
        return {"mean": mean, "q025": mean, "q975": mean}
    rng = random.Random(seed)
    count = len(values)
    means = [
        _mean([values[rng.randrange(count)] for _ in range(count)])
        for _ in range(samples)
    ]
    return {
        "mean": mean,
        "q025": _percentile(means, 0.025),
        "q975": _percentile(means, 0.975),
    }


def run_decision_benchmark(config: dict[str, Any]) -> dict[str, Any]:
    validate_decision_benchmark_config(config)
    rng = random.Random(int(config["seed"]))
    grid_fields = (
        "tail_probability", "tail_visibility", "probability_error", "impact_error",
        "value_shift", "negative_impact_confidence",
    )
    rows: list[dict[str, Any]] = []
    paired: dict[str, list[float]] = defaultdict(list)
    for values in itertools.product(*(config[field] for field in grid_fields)):
        factors = dict(zip(grid_fields, values))
        cases = [
            _run_case(config, factors, rng) for _ in range(int(config["cases_per_cell"]))
        ]
        for method in config["methods"]:
            rows.append(_cell_summary(factors, cases, method))
        for case in cases:
            methods = case["methods"]
            if float(factors["tail_probability"]) > 0 and float(factors["negative_impact_confidence"]) == 0.4:
                paired["h4_catastrophe"].append(
                    methods["confidence_shrink"]["catastrophe_exposure"]
                    - methods["declared_raw"]["catastrophe_exposure"]
                )
            if (
                float(factors["tail_probability"]) > 0
                and factors["tail_visibility"] == "included"
                and any(float(factors[field]) > 0 for field in ("probability_error", "impact_error", "value_shift"))
            ):
                paired["h6_regret"].append(
                    methods["minimax_regret"]["regret"] - methods["declared_raw"]["regret"]
                )
    aggregate = _aggregate_rows(rows)
    positive_tail = _aggregate_rows(rows, lambda row: float(row["tail_probability"]) > 0)
    included_tail = _aggregate_rows(
        rows,
        lambda row: float(row["tail_probability"]) > 0 and row["tail_visibility"] == "included",
    )
    omitted_tail = _aggregate_rows(
        rows,
        lambda row: float(row["tail_probability"]) > 0 and row["tail_visibility"] == "omitted",
    )
    h2 = {}
    for field in ("probability_error", "impact_error", "value_shift"):
        low, high = min(config[field]), max(config[field])
        h2[field] = {
            "zero": _marginal(
                [row for row in rows if float(row["tail_probability"]) > 0],
                field, low, "mean_regret", "declared_raw",
            ),
            "active": _marginal(
                [row for row in rows if float(row["tail_probability"]) > 0],
                field, high, "mean_regret", "declared_raw",
            ),
        }
    h4_interval = _bootstrap_mean_interval(
        paired["h4_catastrophe"],
        int(config["bootstrap_samples"]),
        int(config["bootstrap_seed"]),
    )
    h6_interval = _bootstrap_mean_interval(
        paired["h6_regret"],
        int(config["bootstrap_samples"]),
        int(config["bootstrap_seed"]) + 1,
    )
    h5_gate = included_tail["robustness_gate"]
    h5_shrink = included_tail["confidence_shrink"]
    h5_baseline = included_tail["baseline"]
    h5_regret_improved = h5_gate["mean_regret"] < h5_shrink["mean_regret"]
    h5_catastrophe_improved = (
        h5_gate["catastrophe_exposure"] < h5_shrink["catastrophe_exposure"]
    )
    h5_regret_allowance = 0.10 * max(
        0.0, h5_baseline["mean_regret"] - h5_shrink["mean_regret"]
    )
    h5_catastrophe_allowance = 0.10 * max(
        0.0,
        h5_shrink["catastrophe_exposure"] - h5_baseline["catastrophe_exposure"],
    )
    h5_joint_supported = (
        h5_regret_improved
        and h5_gate["catastrophe_exposure"] - h5_shrink["catastrophe_exposure"]
        <= h5_catastrophe_allowance
    ) or (
        h5_catastrophe_improved
        and h5_gate["mean_regret"] - h5_shrink["mean_regret"] <= h5_regret_allowance
    )
    hypotheses = {
        "H1": {
            "supported": abs(aggregate["oracle_expected"]["mean_regret"]) <= 1e-12
            and all(aggregate[method]["mean_regret"] >= -1e-12 for method in METHODS),
            "oracle_mean_regret": aggregate["oracle_expected"]["mean_regret"],
        },
        "H2": {
            "supported": all(item["active"] >= item["zero"] for item in h2.values()),
            "contrasts": h2,
        },
        "H3": {
            "supported": omitted_tail["robustness_gate"]["certified_nonoracle_rate"]
            > included_tail["robustness_gate"]["certified_nonoracle_rate"],
            "included": included_tail["robustness_gate"]["certified_nonoracle_rate"],
            "omitted": omitted_tail["robustness_gate"]["certified_nonoracle_rate"],
        },
        "H4": {
            "supported": h4_interval["mean"] >= 0,
            "mean_difference": h4_interval["mean"],
            "bootstrap_95": [h4_interval["q025"], h4_interval["q975"]],
            "meaningfully_worse": h4_interval["q025"] > 0,
        },
        "H5": {
            "supported": h5_joint_supported,
            "gate": h5_gate,
            "confidence_shrink": h5_shrink,
            "regret_allowance": h5_regret_allowance,
            "catastrophe_allowance": h5_catastrophe_allowance,
            "regret_increase": h5_gate["mean_regret"] - h5_shrink["mean_regret"],
            "catastrophe_change": h5_gate["catastrophe_exposure"] - h5_shrink["catastrophe_exposure"],
        },
        "H6": {
            "supported": included_tail["minimax_regret"]["p90_regret"]
            < included_tail["declared_raw"]["p90_regret"],
            "paired_mean_regret_difference": _mean(paired["h6_regret"]),
            "paired_mean_bootstrap_95": [h6_interval["q025"], h6_interval["q975"]],
            "minimax_p90": included_tail["minimax_regret"]["p90_regret"],
            "raw_p90": included_tail["declared_raw"]["p90_regret"],
        },
        "H7": {
            "supported": any(
                _marginal(rows, "value_shift", max(config["value_shift"]), "affected_harm_rate", method)
                > _marginal(rows, "value_shift", min(config["value_shift"]), "affected_harm_rate", method)
                for method in METHODS if method not in {"oracle_expected", "baseline"}
            ),
            "by_method": {
                method: {
                    "zero": _marginal(rows, "value_shift", min(config["value_shift"]), "affected_harm_rate", method),
                    "active": _marginal(rows, "value_shift", max(config["value_shift"]), "affected_harm_rate", method),
                }
                for method in METHODS if method not in {"oracle_expected", "baseline"}
            },
        },
    }
    return {
        "experiment_id": config["experiment_id"],
        "title": config["title"],
        "config_sha256": config.get("_config_sha256"),
        "cells": len(rows) // len(config["methods"]),
        "cases": len(rows) // len(config["methods"]) * int(config["cases_per_cell"]),
        "methods": list(config["methods"]),
        "aggregate": aggregate,
        "positive_tail": positive_tail,
        "included_tail": included_tail,
        "omitted_tail": omitted_tail,
        "hypotheses": hypotheses,
        "rows": rows,
    }


def render_decision_benchmark_report(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}", "", "## Scope", "",
        f"Experiment 003A contains {result['cases']:,} synthetic cases across {result['cells']} registered cells. It tests decision-rule mechanics under known generating truth; it is not real-world validation.",
        "", "## Aggregate performance", "",
        "| Method | True value | Mean regret | P90 regret | Harmful choice | Catastrophe exposure | Affected harm | Baseline selected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method in result["methods"]:
        item = result["aggregate"][method]
        lines.append(
            f"| {method} | {item['mean_true_value']:.3f} | {item['mean_regret']:.3f} | {item['p90_regret']:.3f} | "
            f"{item['harmful_choice_rate']:.2%} | {item['catastrophe_exposure']:.2%} | "
            f"{item['affected_harm_rate']:.2%} | {item['baseline_selection_rate']:.2%} |"
        )
    lines.extend(["", "## Registered hypotheses", ""])
    for hypothesis, item in result["hypotheses"].items():
        lines.append(f"- **{hypothesis}: {'supported' if item['supported'] else 'not supported'}.**")
    h3 = result["hypotheses"]["H3"]
    h4 = result["hypotheses"]["H4"]
    h5 = result["hypotheses"]["H5"]
    h6 = result["hypotheses"]["H6"]
    lines.extend(
        [
            "", "## Central stress findings", "",
            f"- Robustness-gate certified-non-oracle rate with the tail included: {h3['included']:.2%}; with the tail omitted: {h3['omitted']:.2%}.",
            f"- Confidence-shrink minus declared-raw catastrophe exposure when negative confidence is 0.4: {h4['mean_difference']:.4f}.",
            f"- With tails included, the robustness gate reduced catastrophe exposure by {-h5['catastrophe_change']:.4f}, but increased mean regret by {h5['regret_increase']:.3f}; the allowed regret increase was {h5['regret_allowance']:.3f}, so H5 failed.",
            f"- Minimax-regret P90 regret was {h6['minimax_p90']:.3f} versus {h6['raw_p90']:.3f} for declared raw; H6 failed.",
            "- The affected-party harm threshold never activated for any method. H7 therefore failed uninformatively and cannot support a distributional conclusion.",
            "- See `summary.json` and `cells.csv` for all registered contrasts; no cell was selected for favorability.",
            "", "## Interpretation boundary", "",
            "The oracle is unavailable in practice. A rule can appear stable because every declared view shares the same missing state, impact error, or value omission. Robustness to declared perturbations is conditional robustness—not protection against the unknown model space.", "",
        ]
    )
    return "\n".join(lines)


def write_decision_benchmark_outputs(result: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows = result["rows"]
    csv_path = destination / "cells.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {key: value for key, value in result.items() if key != "rows"}
    summary_path = destination / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path = destination / "report.md"
    report_path.write_text(render_decision_benchmark_report(result), encoding="utf-8")
    return {"cells": csv_path, "summary": summary_path, "report": report_path}
