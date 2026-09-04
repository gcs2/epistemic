"""Decision-linked analysis for the SES action protocol 0.1."""

from __future__ import annotations

import copy
import json
import math
import random
from pathlib import Path
from typing import Any

from .core import ProtocolError, _normalize, _percentile


def load_decision(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    validate_decision(document)
    return document


def _number(value: Any, location: str, low: float, high: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ProtocolError(f"{location} must be numeric")
    result = float(value)
    if not low <= result <= high:
        raise ProtocolError(f"{location} must be in [{low}, {high}]")
    return result


def _objects_with_unique_ids(document: dict[str, Any], field: str, minimum: int) -> list[dict[str, Any]]:
    items = document.get(field)
    if not isinstance(items, list) or len(items) < minimum:
        raise ProtocolError(f"{field} must contain at least {minimum} item(s)")
    identifiers: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ProtocolError(f"{field}[{index}] must be an object")
        identifier = item.get("id")
        label = item.get("label")
        if not isinstance(identifier, str) or not identifier.strip():
            raise ProtocolError(f"{field}[{index}].id must be a non-empty string")
        if not isinstance(label, str) or not label.strip():
            raise ProtocolError(f"{field}[{index}].label must be a non-empty string")
        identifiers.append(identifier)
    if len(identifiers) != len(set(identifiers)):
        raise ProtocolError(f"{field} contains duplicate ids")
    return items


def validate_decision(document: dict[str, Any]) -> None:
    if not isinstance(document, dict):
        raise ProtocolError("Decision packet must be a JSON object")
    if document.get("protocol_version") != "action-0.1":
        raise ProtocolError("protocol_version must be 'action-0.1'")

    decision = document.get("decision")
    if not isinstance(decision, dict):
        raise ProtocolError("decision must be an object")
    for field in ("title", "question", "owner", "cutoff", "review_date", "baseline_option_id"):
        if not isinstance(decision.get(field), str) or not decision[field].strip():
            raise ProtocolError(f"decision.{field} must be a non-empty string")

    scenarios = _objects_with_unique_ids(document, "scenarios", 2)
    criteria = _objects_with_unique_ids(document, "criteria", 1)
    stakeholders = _objects_with_unique_ids(document, "stakeholders", 1)
    worldviews = _objects_with_unique_ids(document, "worldviews", 1)
    options = _objects_with_unique_ids(document, "options", 2)

    scenario_ids = {item["id"] for item in scenarios}
    criterion_ids = {item["id"] for item in criteria}
    stakeholder_ids = {item["id"] for item in stakeholders}
    option_ids = {item["id"] for item in options}
    if decision["baseline_option_id"] not in option_ids:
        raise ProtocolError("decision.baseline_option_id must name an option")

    for field, items in (("criteria", criteria), ("stakeholders", stakeholders), ("worldviews", worldviews)):
        for index, item in enumerate(items):
            weight = item.get("weight")
            if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
                raise ProtocolError(f"{field}[{index}].weight must be positive")

    for index, worldview in enumerate(worldviews):
        probabilities = worldview.get("scenario_probabilities")
        if not isinstance(probabilities, dict) or set(probabilities) != scenario_ids:
            raise ProtocolError(
                f"worldviews[{index}].scenario_probabilities must cover every scenario exactly"
            )
        values = [
            _number(value, f"worldviews[{index}].scenario_probabilities.{key}", 0.0, 1.0)
            for key, value in probabilities.items()
        ]
        if not math.isclose(sum(values), 1.0, abs_tol=1e-9):
            raise ProtocolError(f"worldviews[{index}].scenario_probabilities must sum to 1")

    expected_impacts = {
        (option_id, scenario_id, stakeholder_id, criterion_id)
        for option_id in option_ids
        for scenario_id in scenario_ids
        for stakeholder_id in stakeholder_ids
        for criterion_id in criterion_ids
    }
    impacts = document.get("impacts")
    if not isinstance(impacts, list):
        raise ProtocolError("impacts must be a list")
    seen: set[tuple[str, str, str, str]] = set()
    for index, impact in enumerate(impacts):
        if not isinstance(impact, dict):
            raise ProtocolError(f"impacts[{index}] must be an object")
        key = tuple(impact.get(field) for field in ("option_id", "scenario_id", "stakeholder_id", "criterion_id"))
        if key not in expected_impacts:
            raise ProtocolError(f"impacts[{index}] references an unknown id")
        if key in seen:
            raise ProtocolError(f"impacts[{index}] duplicates an impact cell")
        seen.add(key)
        _number(impact.get("score"), f"impacts[{index}].score", -100.0, 100.0)
        _number(impact.get("confidence"), f"impacts[{index}].confidence", 0.0, 1.0)
    missing = expected_impacts - seen
    if missing:
        raise ProtocolError(f"impacts is missing {len(missing)} required cell(s)")

    safeguards = document.get("safeguards")
    if not isinstance(safeguards, dict):
        raise ProtocolError("safeguards must be an object")
    for field in ("stop_rules", "appeal_process", "affected_party_review"):
        value = safeguards.get(field)
        if isinstance(value, str):
            valid = bool(value.strip())
        else:
            valid = isinstance(value, list) and bool(value) and all(
                isinstance(item, str) and item.strip() for item in value
            )
        if not valid:
            raise ProtocolError(f"safeguards.{field} must be non-empty")

    pilot = document.get("pilot")
    if not isinstance(pilot, dict):
        raise ProtocolError("pilot must be an object")
    for field in ("primary_metric", "measurement_plan", "duration", "success_rule"):
        if not isinstance(pilot.get(field), str) or not pilot[field].strip():
            raise ProtocolError(f"pilot.{field} must be a non-empty string")

    robustness = document.get("robustness", {})
    if not isinstance(robustness, dict):
        raise ProtocolError("robustness must be an object")
    if "samples" in robustness and (
        not isinstance(robustness["samples"], int) or robustness["samples"] < 1
    ):
        raise ProtocolError("robustness.samples must be a positive integer")
    if "seed" in robustness and not isinstance(robustness["seed"], int):
        raise ProtocolError("robustness.seed must be an integer")
    for field in ("weight_jitter", "impact_jitter"):
        if field in robustness and (
            not isinstance(robustness[field], (int, float))
            or isinstance(robustness[field], bool)
            or robustness[field] < 0
        ):
            raise ProtocolError(f"robustness.{field} must be non-negative")
    if "probability_concentration" in robustness and (
        not isinstance(robustness["probability_concentration"], (int, float))
        or isinstance(robustness["probability_concentration"], bool)
        or robustness["probability_concentration"] <= 0
    ):
        raise ProtocolError("robustness.probability_concentration must be positive")
    if "robust_choice_threshold" in robustness:
        _number(
            robustness["robust_choice_threshold"],
            "robustness.robust_choice_threshold",
            0.0,
            1.0,
        )


def _weights(items: list[dict[str, Any]]) -> dict[str, float]:
    return _normalize({item["id"]: float(item["weight"]) for item in items})


def _impact_lookup(document: dict[str, Any]) -> dict[tuple[str, str, str, str], tuple[float, float]]:
    return {
        (
            item["option_id"],
            item["scenario_id"],
            item["stakeholder_id"],
            item["criterion_id"],
        ): (float(item["score"]), float(item["confidence"]))
        for item in document["impacts"]
    }


def score_options(
    document: dict[str, Any],
    *,
    worldview_weights: dict[str, float] | None = None,
    stakeholder_weights: dict[str, float] | None = None,
    criterion_weights: dict[str, float] | None = None,
) -> tuple[dict[str, float], dict[str, dict[str, float]]]:
    """Return ensemble and per-worldview option scores on the declared -100..100 scale."""
    validate_decision(document)
    worldview_weights = _normalize(worldview_weights or _weights(document["worldviews"]))
    stakeholder_weights = _normalize(stakeholder_weights or _weights(document["stakeholders"]))
    criterion_weights = _normalize(criterion_weights or _weights(document["criteria"]))
    lookup = _impact_lookup(document)

    per_worldview: dict[str, dict[str, float]] = {}
    for worldview in document["worldviews"]:
        option_scores: dict[str, float] = {}
        for option in document["options"]:
            total = 0.0
            for scenario_id, probability in worldview["scenario_probabilities"].items():
                for stakeholder_id, stakeholder_weight in stakeholder_weights.items():
                    for criterion_id, criterion_weight in criterion_weights.items():
                        score, confidence = lookup[
                            (option["id"], scenario_id, stakeholder_id, criterion_id)
                        ]
                        # Low-confidence impact claims shrink toward the explicit neutral point.
                        total += (
                            float(probability)
                            * stakeholder_weight
                            * criterion_weight
                            * score
                            * confidence
                        )
            option_scores[option["id"]] = total
        per_worldview[worldview["id"]] = option_scores

    ensemble = {
        option["id"]: sum(
            worldview_weights[worldview_id] * scores[option["id"]]
            for worldview_id, scores in per_worldview.items()
        )
        for option in document["options"]
    }
    return ensemble, per_worldview


def _jitter_weights(items: list[dict[str, Any]], amount: float, rng: random.Random) -> dict[str, float]:
    return _normalize(
        {
            item["id"]: float(item["weight"]) * math.exp(rng.uniform(-amount, amount))
            for item in items
        }
    )


def _sample_document(document: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    sampled = copy.deepcopy(document)
    config = document.get("robustness", {})
    probability_concentration = float(config.get("probability_concentration", 80.0))
    impact_jitter = float(config.get("impact_jitter", 10.0))
    for worldview in sampled["worldviews"]:
        draws = {
            key: rng.gammavariate(max(float(value) * probability_concentration, 0.001), 1.0)
            for key, value in worldview["scenario_probabilities"].items()
        }
        worldview["scenario_probabilities"] = _normalize(draws)
    for impact in sampled["impacts"]:
        scaled_jitter = impact_jitter * (1.0 - float(impact["confidence"]))
        impact["score"] = min(
            100.0,
            max(-100.0, float(impact["score"]) + rng.uniform(-scaled_jitter, scaled_jitter)),
        )
    return sampled


def analyze_decision(document: dict[str, Any]) -> dict[str, Any]:
    validate_decision(document)
    ensemble, per_worldview = score_options(document)
    option_ids = [item["id"] for item in document["options"]]
    baseline_id = document["decision"]["baseline_option_id"]
    worldview_winners = {
        worldview_id: max(scores, key=scores.get) for worldview_id, scores in per_worldview.items()
    }
    max_regret = {
        option_id: max(max(scores.values()) - scores[option_id] for scores in per_worldview.values())
        for option_id in option_ids
    }

    config = document.get("robustness", {})
    samples = int(config.get("samples", 1000))
    weight_jitter = float(config.get("weight_jitter", 0.25))
    rng = random.Random(int(config.get("seed", 1729)))
    sampled_scores = {option_id: [] for option_id in option_ids}
    wins = {option_id: 0 for option_id in option_ids}
    for _ in range(samples):
        sampled = _sample_document(document, rng)
        scores, _ = score_options(
            sampled,
            worldview_weights=_jitter_weights(document["worldviews"], weight_jitter, rng),
            stakeholder_weights=_jitter_weights(document["stakeholders"], weight_jitter, rng),
            criterion_weights=_jitter_weights(document["criteria"], weight_jitter, rng),
        )
        winner = max(option_ids, key=lambda key: (scores[key], key))
        wins[winner] += 1
        for option_id in option_ids:
            sampled_scores[option_id].append(scores[option_id])

    intervals = {
        option_id: {
            "q05": _percentile(values, 0.05),
            "q50": _percentile(values, 0.50),
            "q95": _percentile(values, 0.95),
        }
        for option_id, values in sampled_scores.items()
    }
    rank_probability = {
        option_id: wins[option_id] / samples for option_id in option_ids
    }
    ranking = sorted(option_ids, key=ensemble.get, reverse=True)
    winner = ranking[0]
    uncertainty_laundering_cells = [
        {
            "option_id": impact["option_id"],
            "scenario_id": impact["scenario_id"],
            "stakeholder_id": impact["stakeholder_id"],
            "criterion_id": impact["criterion_id"],
        }
        for impact in document["impacts"]
        if float(impact["score"]) < 0 and float(impact["confidence"]) < 1
    ]
    robust_choice = (
        len(set(worldview_winners.values())) == 1
        and rank_probability[winner] >= float(config.get("robust_choice_threshold", 0.8))
        and intervals[winner]["q05"] > intervals[baseline_id]["q05"]
        and not uncertainty_laundering_cells
    )
    option_meta = {item["id"]: item for item in document["options"]}
    safety_flags = [
        option_id
        for option_id in option_ids
        if not bool(option_meta[option_id].get("reversible", False))
        or option_meta[option_id].get("risk_level", "high") == "high"
    ]
    return {
        "protocol_version": document["protocol_version"],
        "decision": document["decision"],
        "ensemble_scores": ensemble,
        "per_worldview_scores": per_worldview,
        "worldview_winners": worldview_winners,
        "max_regret": max_regret,
        "intervals": intervals,
        "rank_probability": rank_probability,
        "ranking": ranking,
        "robust_choice": robust_choice,
        "safety_flags": safety_flags,
        "uncertainty_laundering_cells": uncertainty_laundering_cells,
        "baseline_improvement": ensemble[winner] - ensemble[baseline_id],
    }


def render_decision_markdown(document: dict[str, Any], result: dict[str, Any]) -> str:
    options = {item["id"]: item for item in document["options"]}
    worldviews = {item["id"]: item for item in document["worldviews"]}
    decision = document["decision"]
    winner = result["ranking"][0]
    baseline = decision["baseline_option_id"]
    status = "Robust candidate for a bounded pilot" if result["robust_choice"] else "Contested choice—learn before scaling"
    lines = [
        f"# {decision['title']}",
        "",
        "> Generated by the SES action protocol 0.1. Scores are consequences of declared empirical and value judgments, not objective utility, not authorization, and not permission to act.",
        "",
        "## Decision contract",
        "",
        f"- **Question:** {decision['question']}",
        f"- **Owner:** {decision['owner']}",
        f"- **Evidence cutoff:** {decision['cutoff']}",
        f"- **Review date:** {decision['review_date']}",
        f"- **Status:** {status}",
        "",
        "## Option comparison",
        "",
        "| Rank | Option | Expected score | Sensitivity (5–95%) | First-place probability | Maximum worldview regret |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for rank, option_id in enumerate(result["ranking"], 1):
        interval = result["intervals"][option_id]
        lines.append(
            f"| {rank} | {options[option_id]['label']} | {result['ensemble_scores'][option_id]:.1f} | "
            f"{interval['q05']:.1f} to {interval['q95']:.1f} | "
            f"{result['rank_probability'][option_id]:.1%} | {result['max_regret'][option_id]:.1f} |"
        )
    lines.extend(
        [
            "",
            f"The leading option is **{options[winner]['label']}**, scoring {result['baseline_improvement']:.1f} points above the declared baseline **{options[baseline]['label']}**. This is an input-dependent comparison, not a causal finding.",
            "",
            "## Model disagreement",
            "",
            "| Worldview | Preferred option | Scores |",
            "|---|---|---|",
        ]
    )
    for worldview_id, scores in result["per_worldview_scores"].items():
        score_text = "; ".join(
            f"{options[key]['label']}: {value:.1f}"
            for key, value in sorted(scores.items(), key=lambda item: item[1], reverse=True)
        )
        lines.append(
            f"| {worldviews[worldview_id]['label']} | {options[result['worldview_winners'][worldview_id]]['label']} | {score_text} |"
        )
    lines.extend(["", "## Safety and reversibility", ""])
    if result.get("uncertainty_laundering_cells"):
        lines.append(
            f"- **Known scoring hazard:** {len(result['uncertainty_laundering_cells'])} negative impact cell(s) have confidence below 1.0. Action protocol 0.1 moves those harms toward zero and can understate downside; the ranking is exploratory and robust certification is disabled."
        )
    if result["safety_flags"]:
        for option_id in result["safety_flags"]:
            lines.append(f"- **Review required:** {options[option_id]['label']} is high-risk or not declared reversible.")
    else:
        lines.append("- All options are declared reversible and below the high-risk category; this declaration still requires human verification.")
    safeguards = document["safeguards"]
    stop_rules = safeguards["stop_rules"] if isinstance(safeguards["stop_rules"], list) else [safeguards["stop_rules"]]
    for rule in stop_rules:
        lines.append(f"- **Stop rule:** {rule}")
    lines.extend(
        [
            f"- **Appeal:** {safeguards['appeal_process']}",
            f"- **Affected-party review:** {safeguards['affected_party_review']}",
            "",
            "## Learning contract",
            "",
            f"- **Primary metric:** {document['pilot']['primary_metric']}",
            f"- **Measurement:** {document['pilot']['measurement_plan']}",
            f"- **Duration:** {document['pilot']['duration']}",
            f"- **Success rule:** {document['pilot']['success_rule']}",
            "",
            "## Decision discipline",
            "",
            "Do not scale from this report alone. Verify the factual inputs, invite affected parties to challenge the value weights and impact scores, run the bounded pilot, record adverse effects, and update or abandon the model after observation.",
            "",
        ]
    )
    return "\n".join(lines)
