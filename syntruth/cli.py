"""Command-line interface for the SES reference harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .benchmark import load_benchmark_config, run_benchmark, write_benchmark_outputs
from .core import ProtocolError, analyze, load_inquiry, render_markdown
from .decision import analyze_decision, render_decision_markdown, validate_decision
from .decision_v2 import (
    analyze_decision_v2,
    render_decision_v2_markdown,
    validate_decision_v2,
)
from .decision_benchmark import (
    load_decision_benchmark_config,
    run_decision_benchmark,
    write_decision_benchmark_outputs,
)
from .integrity import verify_manifest
from .provenance import load_provenance_config, run_provenance_benchmark, write_provenance_outputs


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="syntruth",
        description="Run a transparent, multi-model epistemic synthesis inquiry.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate an SES inquiry JSON file")
    validate_parser.add_argument("inquiry", type=Path)

    run_parser = subparsers.add_parser("run", help="Analyze an SES inquiry")
    run_parser.add_argument("inquiry", type=Path)
    run_parser.add_argument("--output", "-o", type=Path, help="Write the Markdown report to this path")
    run_parser.add_argument("--json", dest="json_output", type=Path, help="Also write raw results as JSON")

    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Run a preregistered synthetic synthesis benchmark"
    )
    benchmark_parser.add_argument("config", type=Path)
    benchmark_parser.add_argument("--output-dir", "-o", required=True, type=Path)

    verify_parser = subparsers.add_parser("verify", help="Verify a SHA-256 artifact manifest")
    verify_parser.add_argument("manifest", type=Path)

    provenance_parser = subparsers.add_parser(
        "provenance-benchmark", help="Run the Experiment 002A provenance recovery benchmark"
    )
    provenance_parser.add_argument("config", type=Path)
    provenance_parser.add_argument("--output-dir", "-o", required=True, type=Path)

    decision_validate = subparsers.add_parser(
        "decision-validate", help="Validate an SES action protocol packet"
    )
    decision_validate.add_argument("decision", type=Path)

    decide_parser = subparsers.add_parser(
        "decide", help="Analyze an SES action protocol packet"
    )
    decide_parser.add_argument("decision", type=Path)
    decide_parser.add_argument("--output", "-o", type=Path, help="Write the Markdown brief")
    decide_parser.add_argument("--json", dest="json_output", type=Path, help="Write raw results")

    decision_benchmark_parser = subparsers.add_parser(
        "decision-benchmark", help="Run the Experiment 003A decision stress benchmark"
    )
    decision_benchmark_parser.add_argument("config", type=Path)
    decision_benchmark_parser.add_argument("--output-dir", "-o", required=True, type=Path)
    return parser


def _load_action_packet(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    version = document.get("protocol_version") if isinstance(document, dict) else None
    if version == "action-0.1":
        validate_decision(document)
    elif version == "action-0.2":
        validate_decision_v2(document)
    else:
        raise ProtocolError("protocol_version must be 'action-0.1' or 'action-0.2'")
    return document


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "verify":
            records = verify_manifest(args.manifest)
            for record in records:
                status = "OK" if record["valid"] else "FAILED"
                print(f"{status} {record['file']}")
            return 0 if all(record["valid"] for record in records) else 1

        if args.command == "benchmark":
            config = load_benchmark_config(args.config)
            result = run_benchmark(config)
            paths = write_benchmark_outputs(result, args.output_dir)
            for label, path in paths.items():
                print(f"Wrote {label} to {path}")
            return 0

        if args.command == "provenance-benchmark":
            config = load_provenance_config(args.config)
            result = run_provenance_benchmark(config)
            paths = write_provenance_outputs(result, args.output_dir)
            for label, path in paths.items():
                print(f"Wrote {label} to {path}")
            return 0

        if args.command in {"decision-validate", "decide"}:
            document = _load_action_packet(args.decision)
            if args.command == "decision-validate":
                print(f"Valid SES {document['protocol_version']} decision: {document['decision']['title']}")
                return 0
            if document["protocol_version"] == "action-0.2":
                result = analyze_decision_v2(document)
                report = render_decision_v2_markdown(document, result)
            else:
                result = analyze_decision(document)
                report = render_decision_markdown(document, result)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(report, encoding="utf-8")
                print(f"Wrote decision brief to {args.output}")
            else:
                print(report)
            if args.json_output:
                args.json_output.parent.mkdir(parents=True, exist_ok=True)
                args.json_output.write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(f"Wrote raw results to {args.json_output}")
            return 0

        if args.command == "decision-benchmark":
            config = load_decision_benchmark_config(args.config)
            result = run_decision_benchmark(config)
            paths = write_decision_benchmark_outputs(result, args.output_dir)
            for label, path in paths.items():
                print(f"Wrote {label} to {path}")
            return 0

        document = load_inquiry(args.inquiry)
        if args.command == "validate":
            print(f"Valid SES {document['protocol_version']} inquiry: {document['inquiry']['title']}")
            return 0

        result = analyze(document)
        report = render_markdown(document, result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(f"Wrote report to {args.output}")
        else:
            print(report)
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(f"Wrote raw results to {args.json_output}")
        return 0
    except (OSError, json.JSONDecodeError, ProtocolError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
