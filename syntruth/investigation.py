"""Finite Bayesian investigation protocol 0.1; model-conditional planning."""
from __future__ import annotations

import copy
import json
import math
import random
from pathlib import Path

from .core import ProtocolError

VERSION = "investigation-0.1"
METHODS = ("stop", "fixed", "random", "entropy", "myopic", "sequential")


def number(value, location, low=0, high=float("inf")):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProtocolError(f"{location} must be a finite number")
    if not math.isfinite(value) or not low <= value <= high:
        raise ProtocolError(f"{location} out of range")
    return value


def probability_vector(values, keys, location):
    if not isinstance(values, dict) or set(values) != set(keys):
        raise ProtocolError(f"{location} must cover all ids exactly")
    for value in values.values():
        number(value, location, 0, 1)
    if not math.isclose(sum(values.values()), 1, abs_tol=1e-10):
        raise ProtocolError(f"{location} must sum to one")


def ids(items, location):
    if not isinstance(items, list) or not items:
        raise ProtocolError(f"{location} must be a nonempty list")
    found = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            raise ProtocolError(f"{location} requires nonempty ids")
        found.append(item["id"])
    if len(set(found)) != len(found):
        raise ProtocolError(f"{location} has duplicate ids")
    return found


def outcome_metrics(atoms, weights, alpha=.05, severe_threshold=-25):
    """Exact discrete outcome mixture; partial atom mass at a tail boundary."""
    probability_vector(weights, weights, "weights")
    number(alpha, "alpha", 1e-12, 1)
    if not atoms:
        raise ProtocolError("Outcome distribution cannot be empty")
    total = 0
    scored = []
    stakeholder = {s: 0.0 for s in weights}
    for atom in atoms:
        p = number(atom["p"], "outcome probability", 0, 1)
        if set(atom["scores"]) != set(weights):
            raise ProtocolError("Outcome scores must cover stakeholder ids")
        for s, value in atom["scores"].items():
            number(value, "outcome score", -1e6, 1e6)
            stakeholder[s] += p * value
        value = sum(weights[s] * atom["scores"][s] for s in weights)
        scored.append((value, p))
        total += p
    if not math.isclose(total, 1, abs_tol=1e-10):
        raise ProtocolError("Outcome probabilities must sum to one")
    remaining, tail_sum = alpha, 0.0
    for value, p in sorted(scored):
        mass = min(remaining, p)
        tail_sum += mass * value
        remaining -= mass
        if remaining <= 1e-12:
            break
    return {
        "expected_utility": sum(v * p for v, p in scored),
        "outcome_lower_tail_mean": tail_sum / alpha,
        "severe_loss_probability": sum(p for v, p in scored if v < severe_threshold),
        "stakeholder_expected_scores": stakeholder,
        "worst_group_expected_score": min(stakeholder.values()),
    }


def validate(packet):
    if not isinstance(packet, dict) or packet.get("protocol_version") != VERSION:
        raise ProtocolError(f"protocol_version must be {VERSION}")
    if not isinstance(packet.get("title"), str) or not packet["title"].strip():
        raise ProtocolError("title required")
    hypotheses = ids(packet.get("hypotheses"), "hypotheses")
    actions = ids(packet.get("actions"), "actions")
    ids(packet.get("tests"), "tests")
    if len(packet["tests"]) > 8:
        raise ProtocolError("Reference solver supports at most eight tests")
    probability_vector(packet.get("prior"), hypotheses, "prior")
    weights = packet.get("stakeholder_weights")
    if not isinstance(weights, dict) or not weights or any(not isinstance(s, str) or not s for s in weights):
        raise ProtocolError("stakeholder_weights requires named groups")
    probability_vector(weights, weights, "stakeholder_weights")
    budget = packet.get("budget")
    if isinstance(budget, bool) or not isinstance(budget, int) or not 0 <= budget <= 8:
        raise ProtocolError("budget must be an integer from zero to eight")
    if packet.get("baseline_action_id") not in actions:
        raise ProtocolError("baseline_action_id must identify an action")
    for test in packet["tests"]:
        if not isinstance(test.get("family"), str) or not test["family"].strip():
            raise ProtocolError("test family required")
        if not isinstance(test.get("source"), str) or not test["source"].strip():
            raise ProtocolError("test source required")
        if isinstance(test.get("units"), bool) or not isinstance(test.get("units"), int) or test["units"] < 1:
            raise ProtocolError("test units must be a positive integer")
        number(test.get("cost"), "test cost")
        likelihood = test.get("positive_probability")
        if not isinstance(likelihood, dict) or set(likelihood) != set(hypotheses):
            raise ProtocolError("test likelihoods must cover hypotheses")
        for p in likelihood.values():
            number(p, "test likelihood", 0, 1)
    constraints = packet.get("constraints")
    if not isinstance(constraints, list):
        raise ProtocolError("constraints must be a list")
    for constraint in constraints:
        if constraint.get("stakeholder_id") not in weights:
            raise ProtocolError("unknown constrained stakeholder")
        number(constraint.get("floor"), "stakeholder floor", -1e6, 1e6)
        number(constraint.get("max_probability"), "constraint probability", 0, 1)
    for action in packet["actions"]:
        outcomes = action.get("outcomes")
        if not isinstance(outcomes, dict) or set(outcomes) != set(hypotheses):
            raise ProtocolError("action outcomes must cover all hypotheses")
        for atoms in outcomes.values():
            if not isinstance(atoms, list):
                raise ProtocolError("outcomes must be a list")
            outcome_metrics(atoms, weights)
    baseline = next(a for a in packet["actions"] if a["id"] == packet["baseline_action_id"])
    # A feasible fallback is required under every represented hypothesis.
    for atoms in baseline["outcomes"].values():
        if not feasible(packet, atoms):
            raise ProtocolError("baseline violates a declared constraint")


def load(path):
    packet = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(packet)
    return packet


def mixture(action, belief):
    return [
        {"p": belief[h] * atom["p"], "scores": atom["scores"]}
        for h in belief for atom in action["outcomes"][h]
    ]


def feasible(packet, atoms):
    return all(
        sum(a["p"] for a in atoms if a["scores"][c["stakeholder_id"]] < c["floor"])
        <= c["max_probability"] + 1e-12
        for c in packet["constraints"]
    )


def terminal(packet, belief):
    evaluated = []
    for action in packet["actions"]:
        atoms = mixture(action, belief)
        if feasible(packet, atoms):
            evaluated.append((action["id"], outcome_metrics(atoms, packet["stakeholder_weights"])))
    if not evaluated:
        raise ProtocolError("No feasible terminal action")
    # Stable lexical tie rule, never used to inflate an acceptance probability.
    return min(evaluated, key=lambda item: (-item[1]["expected_utility"], item[0]))


def update(belief, test, positive):
    mass = {h: belief[h] * (test["positive_probability"][h] if positive
                            else 1 - test["positive_probability"][h]) for h in belief}
    p = sum(mass.values())
    if p <= 0:
        raise ProtocolError("Observation has zero probability under the declared model")
    return {h: mass[h] / p for h in mass}


def available(packet, spent_units, used_families):
    return [t for t in packet["tests"]
            if t["family"] not in used_families and t["units"] + spent_units <= packet["budget"]]


def entropy(belief):
    return -sum(p * math.log(p) for p in belief.values() if p > 0)


def choose(packet, belief, spent_units=0, used_families=(), method="myopic", rng=None):
    if method not in METHODS:
        raise ProtocolError(f"Unknown investigation policy: {method}")
    counter = [0]

    def solve(b, units, used, depth):
        counter[0] += 1
        _, metrics = terminal(packet, b)
        stop_value = metrics["expected_utility"]
        candidates = {}
        for test in available(packet, units, used):
            p = sum(b[h] * test["positive_probability"][h] for h in b)
            expectation = 0.0
            for positive, mass in ((True, p), (False, 1 - p)):
                if mass <= 0:
                    continue
                after = update(b, test, positive)
                if depth > 1:
                    value = solve(after, units + test["units"], (*used, test["family"]), depth - 1)[1]
                else:
                    value = terminal(packet, after)[1]["expected_utility"]
                expectation += mass * value
            candidates[test["id"]] = expectation - test["cost"]
        best = min(candidates, key=lambda k: (-candidates[k], k)) if candidates else None
        if best is None or candidates[best] <= stop_value + 1e-10:
            return None, stop_value, candidates
        return best, candidates[best], candidates

    tests = available(packet, spent_units, used_families)
    stop_value = terminal(packet, belief)[1]["expected_utility"]
    candidates = {}
    if not tests or method == "stop":
        selected = None
    elif method == "fixed":
        selected = tests[0]["id"]
    elif method == "random":
        if rng is None:
            raise ProtocolError("random policy requires an explicit seeded RNG")
        selected = rng.choice(tests)["id"]
    elif method == "entropy":
        for test in tests:
            p = sum(belief[h] * test["positive_probability"][h] for h in belief)
            after = sum(mass * entropy(update(belief, test, obs))
                        for obs, mass in ((True, p), (False, 1 - p)) if mass > 0)
            candidates[test["id"]] = (entropy(belief) - after) / max(test["cost"], 1e-12)
        selected = min(candidates, key=lambda k: (-candidates[k], k))
        if candidates[selected] <= 1e-10:
            selected = None
    else:
        depth = 1 if method == "myopic" else packet["budget"] - spent_units
        selected, _, candidates = solve(belief, spent_units, tuple(used_families), depth)
    return {"test_id": selected, "stop_expected_utility": stop_value,
            "candidate_values": candidates, "planner_nodes": counter[0],
            "candidate_value_kind": "entropy_gain_per_cost" if method == "entropy"
                                    else "net_expected_utility" if method in {"myopic", "sequential"}
                                    else "fixed_rule",
            "scope": "conditional on supplied hypotheses, likelihoods, outcomes and constraints"}


def replay(packet, method, observe, seed=0):
    """Observe is called only for the selected public test id; truth stays outside."""
    validate(packet)
    belief = copy.deepcopy(packet["prior"])
    used, units, cost, nodes, history = [], 0, 0.0, 0, []
    rng = random.Random(seed)
    while True:
        choice = choose(packet, belief, units, used, method, rng)
        nodes += choice["planner_nodes"]
        if choice["test_id"] is None:
            break
        test = next(t for t in packet["tests"] if t["id"] == choice["test_id"])
        positive = observe(test["id"])
        if not isinstance(positive, bool):
            raise ProtocolError("Observation must be boolean")
        prior = belief.copy()
        belief = update(belief, test, positive)
        units += test["units"]
        cost += test["cost"]
        used.append(test["family"])
        history.append({"test_id": test["id"], "family": test["family"],
                        "positive": positive, "prior": prior, "posterior": belief.copy(),
                        "cost": test["cost"], "choice": choice})
    action, metrics = terminal(packet, belief)
    return {"protocol_version": VERSION, "method": method, "action_id": action,
            "posterior": belief, "history": history, "cost": cost, "units": units,
            "planner_nodes": nodes, "predicted_outcomes": metrics,
            "predicted_net_utility": metrics["expected_utility"] - cost,
            "stop_reason": choice, "authorization": False,
            "scope": "finite declared model; no guarantee for absent mechanisms"}

