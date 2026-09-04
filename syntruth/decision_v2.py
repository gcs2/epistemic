"""Bounded Decision Assurance reference engine for SES action protocol 0.2.

The engine deliberately keeps evidence quality outside consequence arithmetic.
It samples explicitly declared consequence and value ranges, reports a performance
vector, and limits assurance language to a declared challenge set.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

from .core import ProtocolError, _normalize, _percentile


PROTOCOL_VERSION = "action-0.2"


def load_decision_v2(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    validate_decision_v2(document)
    return document


def _number(
    value: Any,
    location: str,
    low: float,
    high: float,
    *,
    low_inclusive: bool = True,
    high_inclusive: bool = True,
) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ProtocolError(f"{location} must be numeric")
    result = float(value)
    low_ok = result >= low if low_inclusive else result > low
    high_ok = result <= high if high_inclusive else result < high
    if not low_ok or not high_ok:
        left = "[" if low_inclusive else "("
        right = "]" if high_inclusive else ")"
        raise ProtocolError(f"{location} must be in {left}{low}, {high}{right}")
    return result


def _non_empty(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(f"{location} must be a non-empty string")
    return value


def _objects_with_unique_ids(
    document: dict[str, Any], field: str, minimum: int
) -> list[dict[str, Any]]:
    items = document.get(field)
    if not isinstance(items, list) or len(items) < minimum:
        raise ProtocolError(f"{field} must contain at least {minimum} item(s)")
    identifiers: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ProtocolError(f"{field}[{index}] must be an object")
        identifiers.append(_non_empty(item.get("id"), f"{field}[{index}].id"))
    if len(identifiers) != len(set(identifiers)):
        raise ProtocolError(f"{field} contains duplicate ids")
    return items


def _validate_range(spec: Any, location: str, low: float, high: float) -> None:
    if not isinstance(spec, dict) or set(spec) != {"low", "central", "high"}:
        raise ProtocolError(f"{location} must contain exactly low, central, and high")
    lower = _number(spec["low"], f"{location}.low", low, high)
    central = _number(spec["central"], f"{location}.central", low, high)
    upper = _number(spec["high"], f"{location}.high", low, high)
    if not lower <= central <= upper:
        raise ProtocolError(f"{location} must satisfy low <= central <= high")


def _validate_weighted(items: list[dict[str, Any]], field: str) -> None:
    for index, item in enumerate(items):
        _non_empty(item.get("label"), f"{field}[{index}].label")
        _validate_range(item.get("weight"), f"{field}[{index}].weight", 0.0, 1_000_000.0)
        if float(item["weight"]["central"]) <= 0:
            raise ProtocolError(f"{field}[{index}].weight.central must be positive")


def _validate_string_list(value: Any, location: str, *, minimum: int = 1) -> list[str]:
    if (
        not isinstance(value, list)
        or len(value) < minimum
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise ProtocolError(f"{location} must be a list of at least {minimum} non-empty string(s)")
    return value


def validate_decision_v2(document: dict[str, Any]) -> None:
    if not isinstance(document, dict):
        raise ProtocolError("Decision packet must be a JSON object")
    if document.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError(f"protocol_version must be '{PROTOCOL_VERSION}'")

    decision = document.get("decision")
    if not isinstance(decision, dict):
        raise ProtocolError("decision must be an object")
    for field in (
        "title",
        "question",
        "owner",
        "cutoff",
        "horizon",
        "baseline_option_id",
    ):
        _non_empty(decision.get(field), f"decision.{field}")

    scenarios = _objects_with_unique_ids(document, "scenarios", 2)
    worldviews = _objects_with_unique_ids(document, "worldviews", 1)
    criteria = _objects_with_unique_ids(document, "criteria", 1)
    stakeholders = _objects_with_unique_ids(document, "stakeholders", 1)
    options = _objects_with_unique_ids(document, "options", 2)
    evidence = _objects_with_unique_ids(document, "evidence", 1)
    challenges = _objects_with_unique_ids(document, "challenges", 1)
    deficits = _objects_with_unique_ids(document, "deficits", 0)

    scenario_ids = {item["id"] for item in scenarios}
    criterion_ids = {item["id"] for item in criteria}
    stakeholder_ids = {item["id"] for item in stakeholders}
    option_ids = {item["id"] for item in options}
    evidence_ids = {item["id"] for item in evidence}
    if decision["baseline_option_id"] not in option_ids:
        raise ProtocolError("decision.baseline_option_id must name an option")

    _validate_weighted(worldviews, "worldviews")
    _validate_weighted(criteria, "criteria")
    _validate_weighted(stakeholders, "stakeholders")

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
        if "probability_concentration" in worldview:
            _number(
                worldview["probability_concentration"],
                f"worldviews[{index}].probability_concentration",
                0.0,
                1_000_000.0,
                low_inclusive=False,
            )

    for index, option in enumerate(options):
        _non_empty(option.get("label"), f"options[{index}].label")
        if not isinstance(option.get("reversible"), bool):
            raise ProtocolError(f"options[{index}].reversible must be boolean")
        if option.get("risk_level") not in {"low", "medium", "high"}:
            raise ProtocolError(f"options[{index}].risk_level must be low, medium, or high")
        if option.get("action_type", "fixed") not in {"fixed", "pilot", "learn", "adaptive"}:
            raise ProtocolError(
                f"options[{index}].action_type must be fixed, pilot, learn, or adaptive"
            )

    for index, item in enumerate(evidence):
        _non_empty(item.get("label"), f"evidence[{index}].label")
        _non_empty(item.get("source"), f"evidence[{index}].source")
        _non_empty(item.get("independence_group"), f"evidence[{index}].independence_group")
        if item.get("quality") not in {"strong", "moderate", "weak", "unknown"}:
            raise ProtocolError(
                f"evidence[{index}].quality must be strong, moderate, weak, or unknown"
            )
        if item.get("status") not in {"supporting", "contested", "refuted"}:
            raise ProtocolError(
                f"evidence[{index}].status must be supporting, contested, or refuted"
            )

    expected = {
        (option_id, scenario_id, stakeholder_id, criterion_id)
        for option_id in option_ids
        for scenario_id in scenario_ids
        for stakeholder_id in stakeholder_ids
        for criterion_id in criterion_ids
    }
    consequences = document.get("consequences")
    if not isinstance(consequences, list):
        raise ProtocolError("consequences must be a list")
    seen: set[tuple[str, str, str, str]] = set()
    for index, consequence in enumerate(consequences):
        if not isinstance(consequence, dict):
            raise ProtocolError(f"consequences[{index}] must be an object")
        key = tuple(
            consequence.get(field)
            for field in ("option_id", "scenario_id", "stakeholder_id", "criterion_id")
        )
        if key not in expected:
            raise ProtocolError(f"consequences[{index}] references an unknown id")
        if key in seen:
            raise ProtocolError(f"consequences[{index}] duplicates a consequence cell")
        seen.add(key)
        _validate_range(consequence.get("estimate"), f"consequences[{index}].estimate", -100.0, 100.0)
        _non_empty(consequence.get("uncertainty_group"), f"consequences[{index}].uncertainty_group")
        references = _validate_string_list(
            consequence.get("evidence_ids"), f"consequences[{index}].evidence_ids"
        )
        unknown = set(references) - evidence_ids
        if unknown:
            raise ProtocolError(f"consequences[{index}].evidence_ids contains unknown ids")
    missing = expected - seen
    if missing:
        raise ProtocolError(f"consequences is missing {len(missing)} required cell(s)")

    for index, challenge in enumerate(challenges):
        _non_empty(challenge.get("label"), f"challenges[{index}].label")
        _non_empty(challenge.get("type"), f"challenges[{index}].type")
        if challenge.get("status") not in {"tested", "bounded", "open"}:
            raise ProtocolError(f"challenges[{index}].status must be tested, bounded, or open")
        _non_empty(challenge.get("method"), f"challenges[{index}].method")

    for index, deficit in enumerate(deficits):
        _non_empty(deficit.get("description"), f"deficits[{index}].description")
        _non_empty(deficit.get("type"), f"deficits[{index}].type")
        if deficit.get("severity") not in {"low", "medium", "high", "blocker"}:
            raise ProtocolError(
                f"deficits[{index}].severity must be low, medium, high, or blocker"
            )
        if deficit.get("status") not in {"open", "resolved", "accepted"}:
            raise ProtocolError(
                f"deficits[{index}].status must be open, resolved, or accepted"
            )

    constraints = document.get("constraints", [])
    if not isinstance(constraints, list):
        raise ProtocolError("constraints must be a list")
    constraint_ids: list[str] = []
    for index, constraint in enumerate(constraints):
        if not isinstance(constraint, dict):
            raise ProtocolError(f"constraints[{index}] must be an object")
        constraint_ids.append(_non_empty(constraint.get("id"), f"constraints[{index}].id"))
        if constraint.get("type") != "minimum_stakeholder_score":
            raise ProtocolError(
                f"constraints[{index}].type must be minimum_stakeholder_score"
            )
        if constraint.get("stakeholder_id") not in stakeholder_ids:
            raise ProtocolError(f"constraints[{index}].stakeholder_id is unknown")
        _number(constraint.get("threshold"), f"constraints[{index}].threshold", -100.0, 100.0)
        _number(
            constraint.get("max_violation_probability"),
            f"constraints[{index}].max_violation_probability",
            0.0,
            1.0,
        )
    if len(constraint_ids) != len(set(constraint_ids)):
        raise ProtocolError("constraints contains duplicate ids")

    assurance = document.get("assurance")
    if not isinstance(assurance, dict):
        raise ProtocolError("assurance must be an object")
    _validate_string_list(assurance.get("required_challenge_types"), "assurance.required_challenge_types")
    _validate_string_list(
        assurance.get("block_on_deficit_severities"),
        "assurance.block_on_deficit_severities",
    )
    invalid_severities = set(assurance["block_on_deficit_severities"]) - {
        "low",
        "medium",
        "high",
        "blocker",
    }
    if invalid_severities:
        raise ProtocolError("assurance.block_on_deficit_severities contains invalid values")
    _number(
        assurance.get("rank_acceptability_threshold"),
        "assurance.rank_acceptability_threshold",
        0.0,
        1.0,
    )
    _number(
        assurance.get("tail_alpha"),
        "assurance.tail_alpha",
        0.0,
        0.5,
        low_inclusive=False,
    )

    learning = document.get("learning")
    if not isinstance(learning, dict):
        raise ProtocolError("learning must be an object")
    for field in ("measurement_plan", "review_date", "success_rule"):
        _non_empty(learning.get(field), f"learning.{field}")
    for field in ("triggers", "stop_rules"):
        _validate_string_list(learning.get(field), f"learning.{field}")
    for field in ("appeal_process", "affected_party_review"):
        _non_empty(learning.get(field), f"learning.{field}")

    analysis = document.get("analysis")
    if not isinstance(analysis, dict):
        raise ProtocolError("analysis must be an object")
    if not isinstance(analysis.get("samples"), int) or analysis["samples"] < 1:
        raise ProtocolError("analysis.samples must be a positive integer")
    if not isinstance(analysis.get("seed"), int):
        raise ProtocolError("analysis.seed must be an integer")


def _triangular_from_u(spec: dict[str, Any], u: float) -> float:
    lower = float(spec["low"])
    mode = float(spec["central"])
    upper = float(spec["high"])
    if math.isclose(lower, upper):
        return lower
    fraction = (mode - lower) / (upper - lower)
    if u < fraction:
        return lower + math.sqrt(u * (upper - lower) * (mode - lower))
    return upper - math.sqrt((1.0 - u) * (upper - lower) * (upper - mode))


def _sample_weights(items: list[dict[str, Any]], rng: random.Random) -> dict[str, float]:
    return _normalize(
        {
            item["id"]: _triangular_from_u(item["weight"], rng.random())
            for item in items
        }
    )


def _central_weights(items: list[dict[str, Any]]) -> dict[str, float]:
    return _normalize({item["id"]: float(item["weight"]["central"]) for item in items})


def _sample_probabilities(worldview: dict[str, Any], rng: random.Random) -> dict[str, float]:
    probabilities = {
        key: float(value) for key, value in worldview["scenario_probabilities"].items()
    }
    concentration = worldview.get("probability_concentration")
    if concentration is None:
        return probabilities
    draws = {
        key: (rng.gammavariate(value * float(concentration), 1.0) if value > 0 else 0.0)
        for key, value in probabilities.items()
    }
    return _normalize(draws)


def _consequence_lookup(
    document: dict[str, Any], group_draws: dict[str, float] | None = None
) -> dict[tuple[str, str, str, str], float]:
    lookup: dict[tuple[str, str, str, str], float] = {}
    for item in document["consequences"]:
        key = (
            item["option_id"],
            item["scenario_id"],
            item["stakeholder_id"],
            item["criterion_id"],
        )
        if group_draws is None:
            value = float(item["estimate"]["central"])
        else:
            value = _triangular_from_u(
                item["estimate"], group_draws[item["uncertainty_group"]]
            )
        lookup[key] = value
    return lookup


def _score_once(
    document: dict[str, Any],
    worldview_weights: dict[str, float],
    stakeholder_weights: dict[str, float],
    criterion_weights: dict[str, float],
    scenario_probabilities: dict[str, dict[str, float]],
    consequences: dict[tuple[str, str, str, str], float],
) -> tuple[
    dict[str, float],
    dict[str, dict[str, float]],
    dict[str, dict[str, float]],
]:
    per_worldview: dict[str, dict[str, float]] = {}
    stakeholder_scores: dict[str, dict[str, float]] = {
        option["id"]: {stakeholder["id"]: 0.0 for stakeholder in document["stakeholders"]}
        for option in document["options"]
    }
    for worldview in document["worldviews"]:
        worldview_id = worldview["id"]
        option_scores: dict[str, float] = {}
        for option in document["options"]:
            option_id = option["id"]
            total = 0.0
            for scenario_id, probability in scenario_probabilities[worldview_id].items():
                for stakeholder_id, stakeholder_weight in stakeholder_weights.items():
                    stakeholder_total = 0.0
                    for criterion_id, criterion_weight in criterion_weights.items():
                        value = consequences[
                            (option_id, scenario_id, stakeholder_id, criterion_id)
                        ]
                        stakeholder_total += criterion_weight * value
                    total += probability * stakeholder_weight * stakeholder_total
                    stakeholder_scores[option_id][stakeholder_id] += (
                        worldview_weights[worldview_id] * probability * stakeholder_total
                    )
            option_scores[option_id] = total
        per_worldview[worldview_id] = option_scores
    ensemble = {
        option["id"]: sum(
            worldview_weights[worldview_id] * per_worldview[worldview_id][option["id"]]
            for worldview_id in per_worldview
        )
        for option in document["options"]
    }
    return ensemble, per_worldview, stakeholder_scores


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _lower_tail_mean(values: list[float], alpha: float) -> float:
    ordered = sorted(values)
    count = max(1, math.ceil(len(ordered) * alpha))
    return _mean(ordered[:count])


def analyze_decision_v2(document: dict[str, Any]) -> dict[str, Any]:
    validate_decision_v2(document)
    option_ids = [item["id"] for item in document["options"]]
    stakeholder_ids = [item["id"] for item in document["stakeholders"]]
    baseline_id = document["decision"]["baseline_option_id"]
    rng = random.Random(document["analysis"]["seed"])
    samples = int(document["analysis"]["samples"])
    alpha = float(document["assurance"]["tail_alpha"])

    central_probabilities = {
        worldview["id"]: {
            key: float(value)
            for key, value in worldview["scenario_probabilities"].items()
        }
        for worldview in document["worldviews"]
    }
    central_scores, central_per_worldview, central_stakeholders = _score_once(
        document,
        _central_weights(document["worldviews"]),
        _central_weights(document["stakeholders"]),
        _central_weights(document["criteria"]),
        central_probabilities,
        _consequence_lookup(document),
    )

    score_samples = {option_id: [] for option_id in option_ids}
    regret_samples = {option_id: [] for option_id in option_ids}
    stakeholder_samples = {
        option_id: {stakeholder_id: [] for stakeholder_id in stakeholder_ids}
        for option_id in option_ids
    }
    wins = {option_id: 0 for option_id in option_ids}
    constraints = document.get("constraints", [])
    violations = {
        option_id: {constraint["id"]: 0 for constraint in constraints}
        for option_id in option_ids
    }
    uncertainty_groups = sorted(
        {item["uncertainty_group"] for item in document["consequences"]}
    )

    for _ in range(samples):
        group_draws = {group: rng.random() for group in uncertainty_groups}
        scenario_probabilities = {
            worldview["id"]: _sample_probabilities(worldview, rng)
            for worldview in document["worldviews"]
        }
        scores, _, group_scores = _score_once(
            document,
            _sample_weights(document["worldviews"], rng),
            _sample_weights(document["stakeholders"], rng),
            _sample_weights(document["criteria"], rng),
            scenario_probabilities,
            _consequence_lookup(document, group_draws),
        )
        winner = max(option_ids, key=lambda option_id: (scores[option_id], option_id))
        wins[winner] += 1
        best_score = max(scores.values())
        for option_id in option_ids:
            score_samples[option_id].append(scores[option_id])
            regret_samples[option_id].append(best_score - scores[option_id])
            for stakeholder_id in stakeholder_ids:
                value = group_scores[option_id][stakeholder_id]
                stakeholder_samples[option_id][stakeholder_id].append(value)
            for constraint in constraints:
                stakeholder_value = group_scores[option_id][constraint["stakeholder_id"]]
                if stakeholder_value < float(constraint["threshold"]):
                    violations[option_id][constraint["id"]] += 1

    option_results: dict[str, dict[str, Any]] = {}
    for option_id in option_ids:
        values = score_samples[option_id]
        stakeholder_means = {
            stakeholder_id: _mean(stakeholder_samples[option_id][stakeholder_id])
            for stakeholder_id in stakeholder_ids
        }
        option_results[option_id] = {
            "central_score": central_scores[option_id],
            "mean_score": _mean(values),
            "q05": _percentile(values, 0.05),
            "q50": _percentile(values, 0.50),
            "q95": _percentile(values, 0.95),
            "lower_tail_mean": _lower_tail_mean(values, alpha),
            "rank_acceptability": wins[option_id] / samples,
            "mean_regret": _mean(regret_samples[option_id]),
            "stakeholder_mean_scores": stakeholder_means,
            "worst_stakeholder_mean": min(stakeholder_means.values()),
            "constraint_violation_probability": {
                constraint_id: count / samples
                for constraint_id, count in violations[option_id].items()
            },
            "probability_above_baseline": sum(
                value > baseline
                for value, baseline in zip(
                    score_samples[option_id], score_samples[baseline_id], strict=True
                )
            )
            / samples,
        }

    ranking = sorted(
        option_ids,
        key=lambda option_id: (option_results[option_id]["mean_score"], option_id),
        reverse=True,
    )
    candidate_id = ranking[0]
    option_meta = {item["id"]: item for item in document["options"]}
    evidence_meta = {item["id"]: item for item in document["evidence"]}
    candidate_evidence_ids = sorted(
        {
            evidence_id
            for item in document["consequences"]
            if item["option_id"] == candidate_id
            for evidence_id in item["evidence_ids"]
        }
    )

    warnings: list[str] = []
    blockers: list[str] = []
    for evidence_id in candidate_evidence_ids:
        item = evidence_meta[evidence_id]
        if item["quality"] in {"weak", "unknown"} or item["status"] == "contested":
            warnings.append(
                f"Candidate relies on {item['quality']} or contested evidence: {evidence_id}."
            )
        if item["status"] == "refuted":
            blockers.append(f"Candidate relies on refuted evidence: {evidence_id}.")

    blocked_severities = set(document["assurance"]["block_on_deficit_severities"])
    unresolved_deficits = [
        item for item in document["deficits"] if item["status"] == "open"
    ]
    for deficit in unresolved_deficits:
        if deficit["severity"] in blocked_severities:
            blockers.append(
                f"Open {deficit['severity']} assurance deficit: {deficit['id']}."
            )

    covered_types = {
        item["type"]
        for item in document["challenges"]
        if item["status"] in {"tested", "bounded"}
    }
    missing_challenge_types = sorted(
        set(document["assurance"]["required_challenge_types"]) - covered_types
    )
    for challenge_type in missing_challenge_types:
        blockers.append(f"Required challenge type is not tested or bounded: {challenge_type}.")

    for constraint in constraints:
        probability = option_results[candidate_id]["constraint_violation_probability"][
            constraint["id"]
        ]
        if probability > float(constraint["max_violation_probability"]):
            blockers.append(
                f"Constraint {constraint['id']} violation probability {probability:.3f} "
                f"exceeds {float(constraint['max_violation_probability']):.3f}."
            )

    candidate = option_meta[candidate_id]
    if candidate["risk_level"] == "high":
        blockers.append("High-risk options are not eligible for a bounded pilot status.")
    if not candidate["reversible"]:
        blockers.append("Irreversible options are not eligible for a bounded pilot status.")

    threshold = float(document["assurance"]["rank_acceptability_threshold"])
    acceptance = float(option_results[candidate_id]["rank_acceptability"])
    lower_bound_beats_baseline = (
        candidate_id != baseline_id
        and option_results[candidate_id]["q05"] > option_results[baseline_id]["q05"]
    )
    if blockers:
        status = "blocked"
    elif acceptance >= threshold and lower_bound_beats_baseline:
        status = "pilot-eligible"
    elif acceptance >= threshold:
        status = "conditionally-preferred"
    else:
        status = "exploratory"

    return {
        "protocol_version": PROTOCOL_VERSION,
        "decision": document["decision"],
        "analysis_contract": {
            "samples": samples,
            "seed": document["analysis"]["seed"],
            "tail_alpha": alpha,
            "uncertainty_groups": uncertainty_groups,
            "consequence_sampling": "triangular bounds with shared quantiles inside each declared uncertainty group",
            "evidence_in_arithmetic": False,
        },
        "central_per_worldview_scores": central_per_worldview,
        "central_stakeholder_scores": central_stakeholders,
        "option_results": option_results,
        "ranking": ranking,
        "assurance_case": {
            "candidate_option_id": candidate_id,
            "status": status,
            "scope": {
                "scenario_ids": sorted(item["id"] for item in document["scenarios"]),
                "worldview_ids": sorted(item["id"] for item in document["worldviews"]),
                "challenge_ids": sorted(item["id"] for item in document["challenges"]),
                "required_challenge_types": document["assurance"][
                    "required_challenge_types"
                ],
            },
            "blockers": blockers,
            "warnings": warnings,
            "unresolved_deficit_ids": [item["id"] for item in unresolved_deficits],
            "missing_challenge_types": missing_challenge_types,
            "universal_guarantee": False,
            "authorization": False,
        },
        "learning_contract": document["learning"],
    }


def render_decision_v2_markdown(document: dict[str, Any], result: dict[str, Any]) -> str:
    options = {item["id"]: item for item in document["options"]}
    evidence = {item["id"]: item for item in document["evidence"]}
    decision = document["decision"]
    assurance = result["assurance_case"]
    candidate_id = assurance["candidate_option_id"]
    lines = [
        f"# {decision['title']}",
        "",
        "> Generated by SES Bounded Decision Assurance 0.2. This is a conditional decision aid over the declared scenarios, values, consequence bounds, challenges, and deficits. It is not a universal robustness guarantee and not authorization to act.",
        "",
        "## Decision contract",
        "",
        f"- **Question:** {decision['question']}",
        f"- **Owner:** {decision['owner']}",
        f"- **Evidence cutoff:** {decision['cutoff']}",
        f"- **Horizon:** {decision['horizon']}",
        f"- **Bounded status:** {assurance['status']}",
        f"- **Candidate:** {options[candidate_id]['label']}",
        "",
        "## Performance vector",
        "",
        "| Rank | Option | Mean | 5–95% | Lower-tail mean | First-rank acceptability | Mean regret | Worst stakeholder mean |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, option_id in enumerate(result["ranking"], 1):
        metrics = result["option_results"][option_id]
        lines.append(
            f"| {rank} | {options[option_id]['label']} | {metrics['mean_score']:.1f} | "
            f"{metrics['q05']:.1f} to {metrics['q95']:.1f} | "
            f"{metrics['lower_tail_mean']:.1f} | {metrics['rank_acceptability']:.1%} | "
            f"{metrics['mean_regret']:.1f} | {metrics['worst_stakeholder_mean']:.1f} |"
        )

    lines.extend(["", "## Constraint checks", ""])
    if document.get("constraints"):
        lines.extend(
            [
                "| Option | Constraint | Violation probability | Allowed |",
                "|---|---|---:|---:|",
            ]
        )
        for option_id in result["ranking"]:
            for constraint in document["constraints"]:
                probability = result["option_results"][option_id][
                    "constraint_violation_probability"
                ][constraint["id"]]
                lines.append(
                    f"| {options[option_id]['label']} | {constraint['id']} | "
                    f"{probability:.1%} | {float(constraint['max_violation_probability']):.1%} |"
                )
    else:
        lines.append("No non-compensable constraints were declared; this absence is not evidence that none apply.")

    lines.extend(["", "## Assurance case", ""])
    lines.append(
        "The status is conditional on scenarios "
        + ", ".join(f"`{item}`" for item in assurance["scope"]["scenario_ids"])
        + " and challenge records "
        + ", ".join(f"`{item}`" for item in assurance["scope"]["challenge_ids"])
        + "."
    )
    if assurance["blockers"]:
        lines.append("")
        lines.append("**Blockers**")
        lines.append("")
        lines.extend(f"- {item}" for item in assurance["blockers"])
    if assurance["warnings"]:
        lines.append("")
        lines.append("**Warnings**")
        lines.append("")
        lines.extend(f"- {item}" for item in assurance["warnings"])
    if assurance["unresolved_deficit_ids"]:
        lines.append("")
        lines.append(
            "Unresolved deficits: "
            + ", ".join(f"`{item}`" for item in assurance["unresolved_deficit_ids"])
            + "."
        )

    candidate_evidence_ids = sorted(
        {
            evidence_id
            for item in document["consequences"]
            if item["option_id"] == candidate_id
            for evidence_id in item["evidence_ids"]
        }
    )
    lines.extend(
        [
            "",
            "## Evidence boundary",
            "",
            "Evidence quality is reported here but is not multiplied into consequence magnitude.",
            "",
            "| Evidence | Quality | Status | Dependence group |",
            "|---|---|---|---|",
        ]
    )
    for evidence_id in candidate_evidence_ids:
        item = evidence[evidence_id]
        lines.append(
            f"| {item['label']} | {item['quality']} | {item['status']} | "
            f"{item['independence_group']} |"
        )

    learning = result["learning_contract"]
    lines.extend(
        [
            "",
            "## Adaptive learning contract",
            "",
            f"- **Review date:** {learning['review_date']}",
            f"- **Measurement:** {learning['measurement_plan']}",
            f"- **Success rule:** {learning['success_rule']}",
        ]
    )
    lines.extend(f"- **Trigger:** {item}" for item in learning["triggers"])
    lines.extend(f"- **Stop rule:** {item}" for item in learning["stop_rules"])
    lines.extend(
        [
            f"- **Appeal:** {learning['appeal_process']}",
            f"- **Affected-party review:** {learning['affected_party_review']}",
            "",
            "## Interpretation boundary",
            "",
            "The intervals are sensitivity distributions induced by declared triangular ranges, probability concentrations, value ranges, and uncertainty groups. They are not frequentist confidence intervals and do not include unimagined states. Review the open deficits and challenge coverage before any pilot, and require independent authority for any real action.",
            "",
        ]
    )
    return "\n".join(lines)
