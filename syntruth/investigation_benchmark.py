"""003B public development generator; never a protected confirmation evaluator."""
from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

from .core import ProtocolError
from .integrity import verify_manifest
from .investigation import METHODS, VERSION, outcome_metrics, replay, validate

REGIMES = ("matched", "disclosed_no_signal", "hidden_no_signal", "reversed", "omitted")
HYPOTHESES = ("ordinary", "source_fault", "mechanism_fault")


def make_case(seed, budget=3):
    rng = random.Random(seed)
    prior = {h: rng.uniform(.15, 1) for h in HYPOTHESES}
    total = sum(prior.values())
    prior = {h: p / total for h, p in prior.items()}
    weights = {"public": .7, "staff": .3}
    scale = rng.uniform(.7, 1.3)
    # (public normal outcome, staff normal outcome, severe outcome probability)
    table = {
        "baseline": [(0, 0, 0)] * 3,
        "general": [(20, 4, .01), (12, 5, .30), (8, 4, .20)],
        "source_repair": [(4, -4, .01), (23, 2, .01), (1, -8, .08)],
        "mechanism_repair": [(3, -5, .01), (2, -7, .08), (25, 1, .01)],
    }
    actions = []
    for action_id, rows in table.items():
        outcomes = {}
        for h, (public, staff, tail) in zip(HYPOTHESES, rows):
            outcomes[h] = [
                {"p": 1 - tail, "scores": {"public": public * scale, "staff": staff * scale}},
                {"p": tail, "scores": {"public": -100 * scale, "staff": -20 * scale}},
            ]
        actions.append({"id": action_id, "outcomes": outcomes})
    tests = []
    for index, name in enumerate(("measurement", "source_audit", "mechanism_test")):
        accuracy = rng.uniform(.65, .95)
        tests.append({"id": name, "family": name,
                      "source": "synthetic independently sampled observation",
                      "units": 1, "cost": rng.uniform(.2, 3.0),
                      "positive_probability": {h: accuracy if j == index else 1 - accuracy
                                               for j, h in enumerate(HYPOTHESES)}})
    return {"protocol_version": VERSION, "title": "Illustrative finite fault inquiry",
            "hypotheses": [{"id": h} for h in HYPOTHESES], "prior": prior,
            "stakeholder_weights": weights, "actions": actions, "tests": tests,
            "baseline_action_id": "baseline", "budget": budget,
            "constraints": [{"stakeholder_id": "public", "floor": -20,
                             "max_probability": .15}]}


def actual_case(packet, regime, seed):
    """Private evaluator data. Never passed to a planning function."""
    rng = random.Random(seed)
    h = rng.choices(list(packet["prior"]), list(packet["prior"].values()))[0]
    if regime == "omitted":
        h = "absent_mechanism"
    observations = {}
    for test in packet["tests"]:
        if regime in {"hidden_no_signal", "disclosed_no_signal"}:
            p = .5
        elif regime == "reversed":
            p = 1 - test["positive_probability"][h]
        elif regime == "omitted":
            p = .5
        else:
            p = test["positive_probability"][h]
        observations[test["id"]] = rng.random() < p
    distributions = {}
    for action in packet["actions"]:
        if regime == "omitted":
            distributions[action["id"]] = (
                [{"p": 1., "scores": {"public": 0, "staff": 0}}]
                if action["id"] == "baseline" else
                [{"p": .65, "scores": {"public": 10, "staff": 3}},
                 {"p": .35, "scores": {"public": -120, "staff": -30}}])
        else:
            distributions[action["id"]] = action["outcomes"][h]
    return h, observations, distributions


def bootstrap_mean_interval(values, samples, seed):
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(values, k=len(values))) / len(values)
                   for _ in range(samples))
    # Explicit nearest-rank percentile convention.
    return [means[max(0, int(samples * .025) - 1)], means[min(samples - 1, int(samples * .975))]]


def validate_config(config):
    if config.get("evaluation") != "development":
        raise ProtocolError("This generator is development-only")
    for key in ("seed", "bootstrap_seed", "cases_per_regime", "budget", "bootstrap_samples"):
        value = config.get(key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ProtocolError(f"{key} must be an integer")
    if config["cases_per_regime"] < 1 or not 0 <= config["budget"] <= 8 or config["bootstrap_samples"] < 100:
        raise ProtocolError("Invalid development sample or budget parameters")
    if config.get("regimes") != list(REGIMES) or config.get("methods") != list(METHODS):
        raise ProtocolError("Development comparisons must retain all registered regimes and methods")


def evaluate(config):
    validate_config(config)
    rows, traces = [], []
    for regime in config["regimes"]:
        for case_index in range(config["cases_per_regime"]):
            packet = make_case(config["seed"] + case_index, config["budget"])
            if regime == "disclosed_no_signal":
                for test in packet["tests"]:
                    test["positive_probability"] = {h: .5 for h in HYPOTHESES}
            validate(packet)
            truth, observations, distributions = actual_case(packet, regime, config["seed"] + 100000 + case_index)
            actual = {a: outcome_metrics(d, packet["stakeholder_weights"]) for a, d in distributions.items()}
            oracle = max(m["expected_utility"] for m in actual.values())
            for method in config["methods"]:
                result = replay(packet, method, observations.__getitem__, seed=config["seed"] + case_index)
                metric = actual[result["action_id"]]
                net = metric["expected_utility"] - result["cost"]
                row = {
                    "regime": regime, "case": case_index, "method": method,
                    "action": result["action_id"], "net_utility": net,
                    "regret": oracle - net,
                    "outcome_lower_tail_mean": metric["outcome_lower_tail_mean"],
                    "severe_loss_probability": metric["severe_loss_probability"],
                    "worst_group_expected_score": metric["worst_group_expected_score"],
                    "predicted_net_utility": result["predicted_net_utility"],
                    "latent_brier": sum((result["posterior"].get(h, 0) - (h == truth)) ** 2
                                       for h in (*HYPOTHESES, "absent_mechanism")),
                    "false_low_risk": int(result["predicted_outcomes"]["severe_loss_probability"] < .05
                                         and metric["severe_loss_probability"] > .10),
                    "baseline": int(result["action_id"] == "baseline"),
                    "cost": result["cost"], "steps": len(result["history"]),
                    "planner_nodes": result["planner_nodes"],
                }
                rows.append(row)
                if case_index == 0:
                    traces.append({"regime": regime, "method": method, "trace": result})
    metrics = [k for k in rows[0] if k not in {"regime", "case", "method", "action"}]
    groups, contrasts = [], []
    for regime in config["regimes"]:
        by_method = {m: [r for r in rows if r["regime"] == regime and r["method"] == m]
                     for m in METHODS}
        for method, values in by_method.items():
            groups.append({"regime": regime, "method": method,
                           **{k: sum(r[k] for r in values) / len(values) for k in metrics}})
        for method in METHODS:
            if method == "sequential":
                continue
            differences = [a["net_utility"] - b["net_utility"]
                           for a, b in zip(by_method["sequential"], by_method[method], strict=True)]
            contrasts.append({"regime": regime, "comparator": method,
                              "mean_net_difference": sum(differences) / len(differences),
                              "descriptive_bootstrap_95": bootstrap_mean_interval(
                                  differences, config["bootstrap_samples"], config["bootstrap_seed"])})
    return {"evaluation": "development", "config": config, "groups": groups, "contrasts": contrasts,
            "rows": rows, "sample_traces": traces,
            "boundary": "Known finite model and supplied likelihoods; exposed generator; no novelty or field validation"}


def write_outputs(result, output):
    root = Path(output)
    if root.exists() and any(root.iterdir()):
        raise ProtocolError("Output directory is nonempty; choose a fresh directory")
    root.mkdir(parents=True, exist_ok=True)
    with (root / "episodes.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result["rows"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(result["rows"])
    summary = {k: v for k, v in result.items() if k not in {"rows", "sample_traces"}}
    for name, value in (("summary.json", summary), ("sample-traces.json", result["sample_traces"])):
        (root / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = ["# 003B investigation development evaluation", "",
             "Exposed development generator; descriptive results, not independent confirmation.",
             "Net utility charges actual investigation and specified delay costs. CPU cost is reported",
             "as planner nodes separately. Outcome tail is the mean of per-episode lower-tail means.",
             "", "| Regime | Policy | Net utility | Cost | Steps | Severe loss probability | False low-risk | Planner nodes |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for g in result["groups"]:
        lines.append(f"| {g['regime']} | {g['method']} | {g['net_utility']:.3f} | {g['cost']:.3f} | "
                     f"{g['steps']:.2f} | {g['severe_loss_probability']:.3f} | {g['false_low_risk']:.3f} | {g['planner_nodes']:.1f} |")
    lines += ["", "## Paired comparisons", "",
              "Sequential minus comparator. Percentile bootstrap intervals are descriptive,",
              "paired across cases and unadjusted for multiple comparisons.", "",
              "| Regime | Comparator | Net difference | 95% interval |",
              "|---|---|---:|---|"]
    for c in result["contrasts"]:
        lo, hi = c["descriptive_bootstrap_95"]
        lines.append(f"| {c['regime']} | {c['comparator']} | {c['mean_net_difference']:.3f} | {lo:.3f} to {hi:.3f} |")
    lines += ["", "## Scope", "", result["boundary"],
              "The omitted mechanism is absent from every public hypothesis set.",
              "No method can assign posterior mass to it. Trace samples expose predictions and updates.",
              "Strong performance with supplied accurate likelihoods does not establish how to obtain those likelihoods.",
              ""]
    (root / "report.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    names = ("episodes.csv", "summary.json", "sample-traces.json", "report.md")
    manifest = "\n".join(f"{hashlib.sha256((root / name).read_bytes()).hexdigest()}  {name}" for name in names)
    (root / "MANIFEST.sha256").write_text(manifest + "\n", encoding="utf-8", newline="\n")
    return root / "report.md"


def run_frozen(config_path, output, frozen):
    records = verify_manifest(frozen)
    if not all(r["valid"] for r in records):
        raise ProtocolError("Development freeze does not verify")
    # The validated config must itself be included in this freeze.
    if not any(Path(r["file"]).resolve() == Path(config_path).resolve() for r in records):
        raise ProtocolError("Freeze must include the actual configuration")
    result = evaluate(json.loads(Path(config_path).read_text(encoding="utf-8")))
    result["input_freeze_sha256"] = hashlib.sha256(Path(frozen).read_bytes()).hexdigest()
    return write_outputs(result, output)

