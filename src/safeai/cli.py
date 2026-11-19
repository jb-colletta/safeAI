"""Command-line interface: ``safeai`` (or ``python -m safeai``)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .assessment import load_assessment, make_template
from .framework import FrameworkError, default_path, load_framework, validate_framework
from .report import diff_to_markdown, plan_to_markdown, to_html, to_json, to_markdown
from .scoring import compare, compute, make_plan, validate_assessment
from . import vendor

import yaml


def _write(text: str, out: Optional[str]) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def _load_scored(path: str, framework, strict: bool, quiet: bool = False):
    assessment = load_assessment(Path(path))
    problems = validate_assessment(framework, assessment)
    if problems and not quiet:
        print(f"warning: {len(problems)} problem(s) in {path} (run `safeai check` for details)", file=sys.stderr)
    return compute(framework, assessment, strict=strict)


def cmd_controls(args, framework) -> int:
    for control in framework["controls"]:
        if args.layer and control["layer"] != f"L{args.layer.lstrip('Ll')}":
            continue
        if args.mode != "both" and args.mode not in control["audience"]:
            continue
        print(
            f"{control['id']:<7} {control['severity']:<9} {control['max_guarantee']:<11} {control['title']}"
        )
    return 0


def cmd_init(args, framework) -> int:
    text = make_template(framework, mode=args.mode, name=args.name or "")
    out = args.output
    if out and Path(out).exists() and not args.force:
        print(f"error: {out} already exists (use --force to overwrite)", file=sys.stderr)
        return 1
    _write(text, out)
    return 0


def cmd_check(args, framework) -> int:
    try:
        assessment = load_assessment(Path(args.assessment))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    problems = validate_assessment(framework, assessment)
    for p in problems:
        print(f"  - {p}")
    result = compute(framework, assessment)
    cov = result["coverage"]
    print(f"{cov['answered']} of {cov['applicable']} applicable controls answered.")
    if problems:
        print(f"{len(problems)} problem(s) found.")
        return 1
    print("OK")
    return 0


def cmd_report(args, framework) -> int:
    result = _load_scored(args.assessment, framework, args.strict)
    plan = make_plan(result)
    if args.format == "json":
        text = to_json(result, plan)
    elif args.format == "html":
        text = to_html(result, plan, framework)
    else:
        text = to_markdown(result, plan, framework)
    _write(text, args.output)
    return 0


def cmd_plan(args, framework) -> int:
    result = _load_scored(args.assessment, framework, args.strict)
    plan = make_plan(result)
    _write(plan_to_markdown(result, plan, framework), args.output)
    return 0


def cmd_diff(args, framework) -> int:
    old = _load_scored(args.before, framework, args.strict, quiet=True)
    new = _load_scored(args.after, framework, args.strict, quiet=True)
    _write(diff_to_markdown(compare(old, new)), args.output)
    return 0


def cmd_framework_check(args, framework) -> int:
    path = Path(args.path) if args.path else None
    with open(path or default_path(), encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    problems = validate_framework(data)
    for p in problems:
        print(f"  - {p}")
    if problems:
        return 1
    print(f"OK: {len(data['layers'])} levels, {len(data['controls'])} controls")
    return 0


def cmd_vendor_questions(args, framework) -> int:
    data = vendor.load_questionnaire()
    problems = vendor.validate_questionnaire(data, framework)
    if problems:
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    _write(vendor.to_markdown(data, vendor_name=args.vendor or ""), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="safeai",
        description="Assess gaps in safe AI use and plan how to close them.",
    )
    p.add_argument("--version", action="version", version=f"safeai {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("controls", help="list the controls in the framework")
    s.add_argument("--layer", help="only this level (1-7)")
    s.add_argument("--mode", choices=("organization", "product", "both"), default="both")
    s.set_defaults(func=cmd_controls)

    s = sub.add_parser("init", help="create a blank assessment file to fill in")
    s.add_argument("-o", "--output", help="file to write (default: print to screen)")
    s.add_argument("--mode", choices=("organization", "product", "both"), default="both",
                   help="organization = you use AI tools; product = you build AI features")
    s.add_argument("--name", help="name of the organization or product")
    s.add_argument("--force", action="store_true", help="overwrite an existing file")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("check", help="validate an assessment file")
    s.add_argument("assessment")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("report", help="score an assessment and write a report")
    s.add_argument("assessment")
    s.add_argument("-f", "--format", choices=("md", "html", "json"), default="md")
    s.add_argument("-o", "--output")
    s.add_argument("--strict", action="store_true", help="count unanswered controls as 'none'")
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("plan", help="write a prioritized action plan")
    s.add_argument("assessment")
    s.add_argument("-o", "--output")
    s.add_argument("--strict", action="store_true", help="count unanswered controls as 'none'")
    s.set_defaults(func=cmd_plan)

    s = sub.add_parser("diff", help="compare two assessments to show progress")
    s.add_argument("before")
    s.add_argument("after")
    s.add_argument("-o", "--output")
    s.add_argument("--strict", action="store_true")
    s.set_defaults(func=cmd_diff)

    s = sub.add_parser("vendor-questions", help="write the questions to send an AI vendor")
    s.add_argument("--vendor", help="name of the vendor, for the heading")
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_vendor_questions)

    s = sub.add_parser("framework-check", help="validate a framework file (for contributors)")
    s.add_argument("path", nargs="?", help="framework YAML (default: the bundled one)")
    s.set_defaults(func=cmd_framework_check)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        framework = load_framework()
    except FrameworkError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    try:
        return args.func(args, framework)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
