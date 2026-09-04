"""Deterministic synthesis engine for SES protocol 0.1."""

from __future__ import annotations

import copy
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


class ProtocolError(ValueError):
    """Raised when an inquiry does not satisfy the protocol."""


def load_inquiry(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    validate(document)
    return document


def _probability(value: Any, location: str, *, open_interval: bool = False) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ProtocolError(f"{location} must be numeric")
    number = float(value)
    valid = 0.0 < number < 1.0 if open_interval else 0.0 <= number <= 1.0
    if not valid:
        interval = "(0, 1)" if open_interval else "[0, 1]"
        raise ProtocolError(f"{location} must be in {interval}")
    return number


def _unique_ids(items: list[dict[str, Any]], location: str) -> list[str]:
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ProtocolError(f"{location}[{index}] must be an object")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            raise ProtocolError(f"{location}[{index}].id must be a non-empty string")
        ids.append(identifier)
    if len(ids) != len(set(ids)):
        raise ProtocolError(f"{location} contains duplicate ids")
    return ids


def validate(document: dict[str, Any]) -> None:
    if not isinstance(document, dict):
        raise ProtocolError("Inquiry must be a JSON object")
    if document.get("protocol_version") != "0.1":
        raise ProtocolError("protocol_version must be '0.1'")

    inquiry = document.get("inquiry")
    if not isinstance(inquiry, dict):
        raise ProtocolError("inquiry must be an object")
    for field in ("title", "question", "claim_type", "cutoff", "horizon", "resolution_criteria"):
        if not isinstance(inquiry.get(field), str) or not inquiry[field].strip():
            raise ProtocolError(f"inquiry.{field} must be a non-empty string")

    hypotheses = document.get("hypotheses")
    if not isinstance(hypotheses, list) or len(hypotheses) < 2:
        raise ProtocolError("hypotheses must contain at least two items")
    hypothesis_ids = _unique_ids(hypotheses, "hypotheses")
    for index, hypothesis in enumerate(hypotheses):
        if not isinstance(hypothesis.get("label"), str) or not hypothesis["label"].strip():
            raise ProtocolError(f"hypotheses[{index}].label must be a non-empty string")

    models = document.get("models")
    if not isinstance(models, list) or not models:
        raise ProtocolError("models must contain at least one item")
    _unique_ids(models, "models")
    for index, model in enumerate(models):
        if not isinstance(model.get("label"), str) or not model["label"].strip():
            raise ProtocolError(f"models[{index}].label must be a non-empty string")
        weight = model.get("weight")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
            raise ProtocolError(f"models[{index}].weight must be positive")
        priors = model.get("priors")
        if not isinstance(priors, dict) or set(priors) != set(hypothesis_ids):
            raise ProtocolError(f"models[{index}].priors must cover every hypothesis exactly")
        for hypothesis_id, prior in priors.items():
            _probability(prior, f"models[{index}].priors.{hypothesis_id}", open_interval=True)

    evidence = document.get("evidence")
    if not isinstance(evidence, list):
        raise ProtocolError("evidence must be a list")
    _unique_ids(evidence, "evidence")
    for index, item in enumerate(evidence):
        for field in ("description", "independence_group"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ProtocolError(f"evidence[{index}].{field} must be a non-empty string")
        _probability(item.get("reliability"), f"evidence[{index}].reliability")
        likelihoods = item.get("likelihoods")
        if not isinstance(likelihoods, dict) or set(likelihoods) != set(hypothesis_ids):
            raise ProtocolError(f"evidence[{index}].likelihoods must cover every hypothesis exactly")
        for hypothesis_id, likelihood in likelihoods.items():
            _probability(
                likelihood,
                f"evidence[{index}].likelihoods.{hypothesis_id}",
                open_interval=True,
            )

    robustness = document.get("robustness", {})
    if not isinstance(robustness, dict):
        raise ProtocolError("robustness must be an object")
    if "samples" in robustness and (
        not isinstance(robustness["samples"], int) or robustness["samples"] < 0
    ):
        raise ProtocolError("robustness.samples must be a non-negative integer")
    for field in ("reliability_jitter", "model_weight_jitter"):
        if field in robustness:
            _probability(robustness[field], f"robustness.{field}")
    if "prior_concentration" in robustness and (
        not isinstance(robustness["prior_concentration"], (int, float))
        or robustness["prior_concentration"] <= 0
    ):
        raise ProtocolError("robustness.prior_concentration must be positive")


def _normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if total <= 0:
        raise ProtocolError("Cannot normalize values with a non-positive total")
    return {key: value / total for key, value in values.items()}


def _softmax(log_values: dict[str, float]) -> dict[str, float]:
    maximum = max(log_values.values())
    exponentials = {key: math.exp(value - maximum) for key, value in log_values.items()}
    return _normalize(exponentials)


def _evidence_groups(
    evidence: Iterable[dict[str, Any]], excluded_groups: set[str] | None = None
) -> dict[str, list[dict[str, Any]]]:
    excluded_groups = excluded_groups or set()
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in evidence:
        if item["independence_group"] not in excluded_groups:
            groups[item["independence_group"]].append(item)
    return dict(groups)


def posterior_for_model(
    document: dict[str, Any],
    model: dict[str, Any],
    *,
    excluded_groups: set[str] | None = None,
) -> dict[str, float]:
    hypothesis_ids = [item["id"] for item in document["hypotheses"]]
    priors = _normalize({key: float(value) for key, value in model["priors"].items()})
    log_scores = {key: math.log(priors[key]) for key in hypothesis_ids}

    for items in _evidence_groups(document["evidence"], excluded_groups).values():
        reliability_sum = sum(float(item["reliability"]) for item in items)
        if reliability_sum == 0:
            continue
        group_reliability = reliability_sum / len(items)
        for hypothesis_id in hypothesis_ids:
            weighted_log_likelihood = sum(
                float(item["reliability"]) * math.log(float(item["likelihoods"][hypothesis_id]))
                for item in items
            ) / reliability_sum
            log_scores[hypothesis_id] += group_reliability * weighted_log_likelihood

    return _softmax(log_scores)


def ensemble_posterior(
    document: dict[str, Any], *, excluded_groups: set[str] | None = None
) -> tuple[dict[str, float], dict[str, dict[str, float]]]:
    model_weights = _normalize(
        {model["id"]: float(model["weight"]) for model in document["models"]}
    )
    per_model = {
        model["id"]: posterior_for_model(document, model, excluded_groups=excluded_groups)
        for model in document["models"]
    }
    hypothesis_ids = [item["id"] for item in document["hypotheses"]]
    ensemble = {
        hypothesis_id: sum(
            model_weights[model_id] * posterior[hypothesis_id]
            for model_id, posterior in per_model.items()
        )
        for hypothesis_id in hypothesis_ids
    }
    return _normalize(ensemble), per_model


def _entropy(distribution: dict[str, float]) -> float:
    return -sum(value * math.log(value) for value in distribution.values() if value > 0)


def model_disagreement(per_model: dict[str, dict[str, float]], weights: dict[str, float]) -> float:
    if len(per_model) <= 1:
        return 0.0
    normalized_weights = _normalize(weights)
    hypothesis_ids = list(next(iter(per_model.values())))
    mixture = {
        hypothesis_id: sum(
            normalized_weights[model_id] * distribution[hypothesis_id]
            for model_id, distribution in per_model.items()
        )
        for hypothesis_id in hypothesis_ids
    }
    weighted_entropy = sum(
        normalized_weights[model_id] * _entropy(distribution)
        for model_id, distribution in per_model.items()
    )
    js_divergence = max(0.0, _entropy(mixture) - weighted_entropy)
    return min(1.0, js_divergence / math.log(len(hypothesis_ids)))


def evidence_leverage(document: dict[str, Any], baseline: dict[str, float]) -> list[dict[str, Any]]:
    groups = sorted({item["independence_group"] for item in document["evidence"]})
    result: list[dict[str, Any]] = []
    for group in groups:
        without_group, _ = ensemble_posterior(document, excluded_groups={group})
        changes = {
            hypothesis_id: without_group[hypothesis_id] - baseline[hypothesis_id]
            for hypothesis_id in baseline
        }
        result.append(
            {
                "group": group,
                "max_absolute_change": max(abs(change) for change in changes.values()),
                "changes": changes,
            }
        )
    return sorted(result, key=lambda item: item["max_absolute_change"], reverse=True)


def _percentile(values: list[float], quantile: float) -> float:
    if not values:
        raise ValueError("Percentile requires at least one value")
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _perturb(document: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    perturbed = copy.deepcopy(document)
    config = document.get("robustness", {})
    reliability_jitter = float(config.get("reliability_jitter", 0.1))
    weight_jitter = float(config.get("model_weight_jitter", 0.15))
    prior_concentration = float(config.get("prior_concentration", 80.0))

    for item in perturbed["evidence"]:
        item["reliability"] = min(
            1.0,
            max(0.0, float(item["reliability"]) + rng.uniform(-reliability_jitter, reliability_jitter)),
        )

    for model in perturbed["models"]:
        model["weight"] = float(model["weight"]) * math.exp(rng.uniform(-weight_jitter, weight_jitter))
        normalized_priors = _normalize({key: float(value) for key, value in model["priors"].items()})
        draws = {
            key: rng.gammavariate(max(value * prior_concentration, 0.001), 1.0)
            for key, value in normalized_priors.items()
        }
        model["priors"] = _normalize(draws)

    return perturbed


def robustness_intervals(document: dict[str, Any]) -> dict[str, dict[str, float]]:
    config = document.get("robustness", {})
    samples = int(config.get("samples", 500))
    hypothesis_ids = [item["id"] for item in document["hypotheses"]]
    if samples == 0:
        baseline, _ = ensemble_posterior(document)
        return {
            key: {"q05": value, "q50": value, "q95": value}
            for key, value in baseline.items()
        }
    rng = random.Random(int(config.get("seed", 1729)))
    values = {key: [] for key in hypothesis_ids}
    for _ in range(samples):
        ensemble, _ = ensemble_posterior(_perturb(document, rng))
        for hypothesis_id in hypothesis_ids:
            values[hypothesis_id].append(ensemble[hypothesis_id])
    return {
        key: {
            "q05": _percentile(sample, 0.05),
            "q50": _percentile(sample, 0.50),
            "q95": _percentile(sample, 0.95),
        }
        for key, sample in values.items()
    }


def analyze(document: dict[str, Any]) -> dict[str, Any]:
    validate(document)
    ensemble, per_model = ensemble_posterior(document)
    model_weights = {model["id"]: float(model["weight"]) for model in document["models"]}
    intervals = robustness_intervals(document)
    ranking = sorted(ensemble, key=ensemble.get, reverse=True)
    model_winners = {
        model_id: max(distribution, key=distribution.get)
        for model_id, distribution in per_model.items()
    }
    winner = ranking[0]
    rivals = ranking[1:]
    robust_core = len(set(model_winners.values())) == 1 and all(
        intervals[winner]["q05"] > intervals[rival]["q95"] for rival in rivals
    )
    return {
        "protocol_version": document["protocol_version"],
        "inquiry": document["inquiry"],
        "ensemble": ensemble,
        "per_model": per_model,
        "model_winners": model_winners,
        "disagreement": model_disagreement(per_model, model_weights),
        "robustness": intervals,
        "leverage": evidence_leverage(document, ensemble),
        "ranking": ranking,
        "robust_core": robust_core,
    }


def render_markdown(document: dict[str, Any], result: dict[str, Any]) -> str:
    hypothesis_by_id = {item["id"]: item for item in document["hypotheses"]}
    model_by_id = {item["id"]: item for item in document["models"]}
    inquiry = document["inquiry"]
    lines = [
        f"# {inquiry['title']}",
        "",
        "> Generated by the SES 0.1 reference harness. Numerical results synthesize the supplied judgments; they do not independently establish historical or scientific truth.",
        "",
        "## Inquiry contract",
        "",
        f"- **Question:** {inquiry['question']}",
        f"- **Claim type:** {inquiry['claim_type']}",
        f"- **Evidence cutoff:** {inquiry['cutoff']}",
        f"- **Horizon:** {inquiry['horizon']}",
        f"- **Resolution:** {inquiry['resolution_criteria']}",
        "",
        "## Synthesis",
        "",
        "| Rank | Hypothesis | Ensemble | Sensitivity interval (5–95%) |",
        "|---:|---|---:|---:|",
    ]
    for rank, hypothesis_id in enumerate(result["ranking"], 1):
        interval = result["robustness"][hypothesis_id]
        lines.append(
            f"| {rank} | {hypothesis_by_id[hypothesis_id]['label']} | "
            f"{result['ensemble'][hypothesis_id]:.1%} | "
            f"{interval['q05']:.1%}–{interval['q95']:.1%} |"
        )

    winner = result["ranking"][0]
    status = "Robust core detected" if result["robust_core"] else "Contested shell"
    lines.extend(
        [
            "",
            f"**{status}.** The leading hypothesis is **{hypothesis_by_id[winner]['label']}**. "
            f"Normalized model disagreement is {result['disagreement']:.3f} on a 0–1 scale.",
            "",
            "## Model perspectives",
            "",
            "| Model | Weight | Leading hypothesis | Distribution |",
            "|---|---:|---|---|",
        ]
    )
    normalized_model_weights = _normalize(
        {model["id"]: float(model["weight"]) for model in document["models"]}
    )
    for model_id, distribution in result["per_model"].items():
        distribution_text = "; ".join(
            f"{hypothesis_by_id[key]['label']}: {value:.1%}"
            for key, value in sorted(distribution.items(), key=lambda item: item[1], reverse=True)
        )
        model_winner = result["model_winners"][model_id]
        lines.append(
            f"| {model_by_id[model_id]['label']} | {normalized_model_weights[model_id]:.1%} | "
            f"{hypothesis_by_id[model_winner]['label']} | {distribution_text} |"
        )

    lines.extend(
        [
            "",
            "## Evidence leverage",
            "",
            "Leverage is the largest posterior change when an entire dependence group is removed.",
            "",
            "| Evidence group | Maximum change |",
            "|---|---:|",
        ]
    )
    if result["leverage"]:
        for item in result["leverage"]:
            lines.append(f"| {item['group']} | {item['max_absolute_change']:.1%} |")
    else:
        lines.append("| No evidence groups supplied | 0.0% |")

    if document.get("challenges"):
        lines.extend(["", "## Registered challenges", ""])
        for challenge in document["challenges"]:
            target = challenge.get("target", "inquiry")
            lines.append(f"- **{target}:** {challenge['description']}")

    limitations = inquiry.get("limitations", [])
    if limitations:
        lines.extend(["", "## Declared limitations", ""])
        for limitation in limitations:
            lines.append(f"- {limitation}")

    lines.extend(
        [
            "",
            "## Interpretation discipline",
            "",
            "The sensitivity intervals reflect only the perturbations declared in this inquiry. They do not include unknown hypotheses, fabricated evidence, model misspecification, or unrecorded source dependence. Review the inputs before relying on the result.",
            "",
        ]
    )
    return "\n".join(lines)
