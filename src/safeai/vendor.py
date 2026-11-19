"""Vendor questionnaire: questions to send to an AI vendor, keyed to framework controls."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .framework import FrameworkError

REQUIRED = ("id", "topic", "controls", "ask", "look_for", "red_flag")


def default_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "vendor-questionnaire.yaml"


def load_questionnaire(path: Optional[Path] = None) -> Dict[str, Any]:
    p = Path(path) if path else default_path()
    try:
        with open(p, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise FrameworkError(f"{p} is not valid YAML: {exc}") from exc
    return data


def validate_questionnaire(data: Any, framework: Dict[str, Any]) -> List[str]:
    """Return a list of problems (empty if fine)."""
    problems: List[str] = []
    if not isinstance(data, dict):
        return ["questionnaire is not a mapping"]
    topics = {t.get("id") for t in data.get("topics") or []}
    control_ids = {c["id"] for c in framework["controls"]}
    seen = set()
    for q in data.get("questions") or []:
        qid = q.get("id", "?")
        for field in REQUIRED:
            if not q.get(field):
                problems.append(f"{qid}: missing {field}")
        if qid in seen:
            problems.append(f"{qid}: duplicate id")
        seen.add(qid)
        if q.get("topic") not in topics:
            problems.append(f"{qid}: unknown topic {q.get('topic')!r}")
        for cid in q.get("controls") or []:
            if cid not in control_ids:
                problems.append(f"{qid}: unknown control {cid}")
    if not data.get("questions"):
        problems.append("no questions")
    return problems


def to_markdown(data: Dict[str, Any], vendor_name: str = "") -> str:
    lines: List[str] = []
    title = "AI vendor questions"
    if vendor_name:
        title += f": {vendor_name}"
    lines += [f"# {title}", ""]
    lines += [str(data.get("intro", "")).strip(), ""]
    lines += [
        "Answer each question in writing and attach or link the document it comes from.",
        "",
    ]
    by_topic: Dict[str, List[Dict[str, Any]]] = {}
    for q in data["questions"]:
        by_topic.setdefault(q["topic"], []).append(q)
    for t in data["topics"]:
        qs = by_topic.get(t["id"], [])
        if not qs:
            continue
        lines += [f"## {t['name']}", ""]
        for q in qs:
            lines += [
                f"### {q['id']}. {q['ask']}",
                "",
                f"- **Helps answer:** {', '.join(q['controls'])}",
                f"- **A good answer looks like:** {q['look_for']}",
                f"- **Lowers confidence:** {q['red_flag']}",
                "- **Vendor's answer:**",
                "- **Document or link:**",
                "- **Kind of guarantee (structural / procedural / guided):**",
                "",
            ]
    return "\n".join(lines).rstrip() + "\n"
