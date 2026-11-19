"""Render results as Markdown, HTML, or JSON."""

from __future__ import annotations

import html
import json
from typing import Any, Dict, List

from .framework import controls_by_id
from .scoring import STATUS_TEXT

ANSWER_LABEL = {
    "structural": "Structural",
    "procedural": "Procedural",
    "guided": "Guided",
    "none": "None",
    "na": "N/A",
    "": "Not assessed",
}

DISCLAIMER = (
    "This report is generated from self-reported answers. It is a planning aid, not an "
    "audit, certification, or legal advice. Scores are indicative and depend entirely on "
    "the honesty and accuracy of the answers."
)


def to_json(result: Dict[str, Any], plan: Dict[str, Any]) -> str:
    return json.dumps({"result": result, "plan": plan}, indent=2, ensure_ascii=False) + "\n"


def _fmt(score) -> str:
    return "n/a" if score is None else f"{score:.1f}"


def to_markdown(result: Dict[str, Any], plan: Dict[str, Any], framework: Dict[str, Any]) -> str:
    scope = result["scope"]
    by_id = controls_by_id(framework)
    o = result["overall"]
    cov = result["coverage"]
    lines: List[str] = []
    title = scope.get("name") or "Untitled assessment"
    lines.append(f"# safeAI assessment: {title}")
    lines.append("")
    meta = []
    if scope.get("assessor"):
        meta.append(f"Assessor: {scope['assessor']}")
    if scope.get("date"):
        meta.append(f"Date: {scope['date']}")
    meta.append(f"Mode: {scope.get('mode', 'both')}")
    meta.append(f"Framework version: {result['framework_version']}")
    lines.append(" · ".join(meta))
    lines.append("")
    lines.append(f"> {DISCLAIMER}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    if o["score"] is None:
        lines.append("No controls have been answered yet, so there is no score.")
    else:
        lines.append(f"**Overall: {_fmt(o['score'])} / 100 ({o['band']})**")
        if o["gated"]:
            state = "not met" if result["floor"]["status"] == "not_met" else "not yet confirmed"
            lines.append("")
            lines.append(
                f"**Held at {o['band']}:** the human-dignity floor is {state}. "
                f"Without that, the rating would be {o['ungated_band']}."
            )
    lines.append("")
    if o["score"] is not None and not result["strict"] and cov["percent"] is not None and cov["percent"] < 50:
        lines.append("**Provisional:** fewer than half of the applicable controls have been answered.")
        lines.append("")
    lines.append(
        f"Coverage: {cov['answered']} of {cov['applicable']} applicable controls answered"
        + (f" ({_fmt(cov['percent'])}%)" if cov["percent"] is not None else "")
        + (f"; {cov['not_applicable']} marked not applicable" if cov["not_applicable"] else "")
        + "."
    )
    if cov["answered"] < cov["applicable"] and not result["strict"]:
        lines.append(
            "Unanswered controls are left out of the scores. The real position may be worse "
            "than shown. Use `--strict` to count them as `none`."
        )
    lines.append("")

    lines.append("## What you can honestly say")
    lines.append("")
    lines.append("*The AI is a guest, not an admin.*")
    lines.append("")
    lines.append("| | Statement | Status from your answers |")
    lines.append("|---|---|---|")
    for v in result["verbs"]:
        lines.append(f"| **{v['verb']}** | {v['clause']} | {STATUS_TEXT[v['status']]} ({_fmt(v['score'])}) |")
    lines.append("")
    lines.append(
        "Only describe a control as *enforced* if you answered `structural` and can show the evidence. "
        "Describe `procedural` as *requiring approval* and `guided` as *recommended*."
    )
    lines.append("")

    lines.extend(_floor_markdown(result["floor"]))

    lines.append("## The seven levels")
    lines.append("")
    lines.append("| Level | Score | Structural | Procedural | Guided | None | Not assessed |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for layer in result["layers"]:
        c = layer["counts"]
        lines.append(
            f"| L{layer['number']} {layer['name']} ({layer['verb']}) | {_fmt(layer['score'])} | "
            f"{c['structural']} | {c['procedural']} | {c['guided']} | {c['none']} | {c['unanswered']} |"
        )
    lines.append("")

    if result["unevidenced"]:
        lines.append("## Claims without evidence")
        lines.append("")
        lines.append(
            "These controls were marked procedural or structural with no note or evidence. "
            "Confirm each before you rely on or repeat the claim."
        )
        lines.append("")
        for cid in result["unevidenced"]:
            lines.append(f"- {cid} {by_id[cid]['title']}")
        lines.append("")

    lines.extend(_plan_markdown(plan, by_id, heading_level=2))

    lines.append("## All controls")
    lines.append("")
    lines.append("| ID | Control | Severity | Answer | Strongest possible |")
    lines.append("|---|---|---|---|---|")
    for r in result["controls"]:
        lines.append(
            f"| {r['id']} | {r['title']} | {r['severity']} | {ANSWER_LABEL[r['answer']]} | {r['max_guarantee']} |"
        )
    lines.append("")
    return "\n".join(lines)


FLOOR_STATE = {"met": "Met", "not_met": "Not met", "unconfirmed": "Not assessed", "na": "N/A"}
FLOOR_TEXT = {
    "met": (
        "Every floor control is reported at procedural or stronger. This is a self-reported result, "
        "not a certification, and it does not show that the AI itself behaves well."
    ),
    "not_met": (
        "The floor is **not met**. At least one floor control is answered below procedural. "
        "Close these before anything else."
    ),
    "unconfirmed": (
        "The floor is **not yet confirmed**. Some floor controls are unanswered. "
        "Answer them before relying on any rating."
    ),
}


def _floor_markdown(floor: Dict[str, Any]) -> List[str]:
    if floor["status"] == "none":
        return []
    lines = ["## The human-dignity floor", "", FLOOR_TEXT[floor["status"]], ""]
    lines.append("| ID | What it protects | Control | Your answer | Floor |")
    lines.append("|---|---|---|---|---|")
    for i in floor["controls"]:
        lines.append(
            f"| {i['id']} | {i['principle']} | {i['title']} | {ANSWER_LABEL[i['answer']]} | {FLOOR_STATE[i['state']]} |"
        )
    lines.append("")
    if floor["not_applicable"]:
        lines.append(
            "Marked not applicable (confirm that each really does not apply to you): "
            + ", ".join(floor["not_applicable"]) + "."
        )
        lines.append("")
    return lines


def _plan_markdown(plan: Dict[str, Any], by_id: Dict[str, Any], heading_level: int = 2) -> List[str]:
    h = "#" * heading_level
    lines: List[str] = []
    lines.append(f"{h} Action plan")
    lines.append("")
    if not plan["count"]:
        lines.append("No gaps found among the controls you answered. Keep your evidence current.")
        lines.append("")
        return lines
    if plan.get("floor"):
        lines.append(f"{h}# Human-dignity floor first")
        lines.append("")
        for i in plan["floor"]:
            lines.append(f"- **{i['id']} {i['title']}**: {_move(i)}")
        lines.append("")
    open_critical = [i for i in plan["critical"] if i["current"] in ("none", "unanswered", "guided")]
    if open_critical:
        lines.append(f"{h}# Critical gaps first")
        lines.append("")
        for i in open_critical:
            lines.append(f"- **{i['id']} {i['title']}**: {_move(i)}")
        lines.append("")
    names = {
        "quick": "Quick wins (low effort, weeks)",
        "next": "Build next (medium effort, a few months)",
        "later": "Longer term (high effort)",
    }
    for key in ("quick", "next", "later"):
        items = plan["horizons"][key]
        if not items:
            continue
        lines.append(f"{h}# {names[key]}")
        lines.append("")
        for i in items:
            lines.append(f"**{i['id']} {i['title']}** · {i['severity']} · {_move(i)}")
            for step in by_id[i["id"]]["steps"]:
                lines.append(f"- [ ] {step}")
            lines.append("")
    return lines


def _move(i: Dict[str, Any]) -> str:
    if i["assess_first"]:
        return f"not yet assessed. Answer it first (target: {i['target']})"
    if i["current"] == i["next"]:
        return f"currently {i['current']}"
    return f"currently {i['current']}, next step {i['next']} (target: {i['target']})"


def plan_to_markdown(result: Dict[str, Any], plan: Dict[str, Any], framework: Dict[str, Any]) -> str:
    by_id = controls_by_id(framework)
    title = result["scope"].get("name") or "Untitled assessment"
    lines = [f"# safeAI action plan: {title}", "", f"> {DISCLAIMER}", ""]
    lines.extend(_plan_markdown(plan, by_id, heading_level=2))
    return "\n".join(lines)


def diff_to_markdown(diff: Dict[str, Any]) -> str:
    o = diff["overall"]
    lines = ["# safeAI progress", ""]
    fl = diff.get("floor", {})
    if fl.get("before") != fl.get("after"):
        lines.append(f"Human-dignity floor: {fl.get('before')} → {fl.get('after')}")
        lines.append("")
    lines.append(f"Overall: {_fmt(o['before'])} → {_fmt(o['after'])}" + (f" ({o['delta']:+.1f})" if o["delta"] is not None else ""))
    lines.append("")
    lines.append("| Level | Before | After | Change |")
    lines.append("|---|---:|---:|---:|")
    for layer in diff["layers"]:
        d = "" if layer["delta"] is None else f"{layer['delta']:+.1f}"
        lines.append(f"| {layer['name']} | {_fmt(layer['before'])} | {_fmt(layer['after'])} | {d} |")
    lines.append("")
    lines.append(f"## Gaps closed or narrowed ({len(diff['improved'])})")
    lines.append("")
    for i in diff["improved"]:
        lines.append(f"- {i['id']} {i['title']}: {i['from']} → {i['to']}")
    lines.append("")
    lines.append(f"## Regressions ({len(diff['regressed'])})")
    lines.append("")
    for i in diff["regressed"]:
        lines.append(f"- {i['id']} {i['title']}: {i['from']} → {i['to']}")
    lines.append("")
    return "\n".join(lines)


_CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5c6470;--line:#d9dde3;--accent:#1f5fbf}
@media (prefers-color-scheme:dark){:root{--bg:#14171c;--fg:#e8eaed;--muted:#9aa3ad;--line:#2d333b;--accent:#6ea8ff}}
body{font:16px/1.55 system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:60rem;margin:0 auto;padding:1.5rem 1rem}
table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{border-bottom:1px solid var(--line);padding:.4rem .5rem;text-align:left;vertical-align:top}
blockquote{border-left:3px solid var(--line);margin:1rem 0;padding:.1rem 1rem;color:var(--muted)}
h1,h2,h3{line-height:1.25}a{color:var(--accent)}
"""


def to_html(result: Dict[str, Any], plan: Dict[str, Any], framework: Dict[str, Any]) -> str:
    """A simple, self-contained HTML rendering of the Markdown report."""
    md = to_markdown(result, plan, framework)
    body = _md_to_html(md)
    title = html.escape(result["scope"].get("name") or "Untitled assessment")
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>safeAI assessment: {title}</title><style>{_CSS}</style></head><body>{body}</body></html>\n"
    )


def _inline(text: str) -> str:
    s = html.escape(text)
    out, bold, ital = [], False, False
    i = 0
    while i < len(s):
        if s.startswith("**", i):
            out.append("</strong>" if bold else "<strong>")
            bold = not bold
            i += 2
        elif s[i] == "*":
            out.append("</em>" if ital else "<em>")
            ital = not ital
            i += 1
        elif s[i] == "`":
            j = s.find("`", i + 1)
            if j == -1:
                out.append(s[i])
                i += 1
            else:
                out.append("<code>" + s[i + 1 : j] + "</code>")
                i = j + 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _md_to_html(md: str) -> str:
    """Convert the limited Markdown this module emits (headings, tables, bullets, quotes)."""
    out: List[str] = []
    lines = md.split("\n")
    i = 0
    in_list = False
    while i < len(lines):
        line = lines[i]
        if in_list and not line.startswith("- "):
            out.append("</ul>")
            in_list = False
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{level}>{_inline(line[level:].strip())}</h{level}>")
        elif line.startswith("> "):
            out.append(f"<blockquote><p>{_inline(line[2:])}</p></blockquote>")
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            i -= 1
            out.append(_table(rows))
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            item = line[2:]
            if item.startswith("[ ] "):
                item = "☐ " + item[4:]
            out.append(f"<li>{_inline(item)}</li>")
        elif line.strip():
            out.append(f"<p>{_inline(line)}</p>")
        i += 1
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _table(rows: List[str]) -> str:
    def cells(r: str) -> List[str]:
        return [c.strip() for c in r.strip().strip("|").split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    out = ["<table><thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in header) + "</tr></thead><tbody>"]
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)
