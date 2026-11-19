"""Scoring, validation, action planning, and progress comparison.

The scoring rules are documented in docs/scoring.md. The browser tool uses an
equivalent implementation in web/scoring.js, and the test suite checks that the two
agree on the example assessment.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from .framework import (
    ANSWERS,
    EFFORT_COST,
    GUARANTEE_RANK,
    MODES,
    RANK_NAME,
    SEVERITY_WEIGHT,
    applies,
    controls_by_id,
)

BANDS = (
    (90, "Leading"),
    (75, "Strong"),
    (50, "Developing"),
    (25, "Basic"),
    (0, "Exposed"),
)

VERB_CLAUSES = {
    "SEE": "It sees only what your people are already allowed to see, minus what you wall off.",
    "DO": "It does only what you grant, and it stops for a named person where it matters.",
    "SAY": "It says nothing that contradicts what you stand for, and never poses as a person.",
    "ANSWER": "You answer for it with a full record of every decision, and you can stop it.",
}

STATUS_TEXT = {
    "supported": "Supported by your answers",
    "partly": "Partly supported",
    "not_yet": "Not yet supported",
    "unassessed": "Not assessed",
}


def pct(x: float) -> float:
    """Round a 0..1 fraction to a percentage with one decimal, half up.

    Deliberately not Python's round(): the browser tool must agree to the digit.
    """
    return math.floor(x * 1000 + 0.5) / 10


def r4(x: float) -> float:
    """Round to four decimals, half up (mirrors the browser tool)."""
    return math.floor(x * 10000 + 0.5) / 10000


def band_for(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    for floor, name in BANDS:
        if score >= floor:
            return name
    return BANDS[-1][1]


# ---------------------------------------------------------------- assessment files


def normalize_assessment(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Accept the documented format plus the shorthand ``L1.01: structural``."""
    scope = dict(raw.get("scope") or {})
    scope.setdefault("mode", "both")
    answers: Dict[str, Dict[str, str]] = {}
    for cid, val in (raw.get("answers") or {}).items():
        if isinstance(val, dict):
            ans = val.get("answer")
            answers[str(cid)] = {
                "answer": (str(ans).strip().lower() if ans not in (None, "") else ""),
                "note": str(val.get("note") or ""),
                "evidence": str(val.get("evidence") or ""),
            }
        else:
            answers[str(cid)] = {
                "answer": (str(val).strip().lower() if val not in (None, "") else ""),
                "note": "",
                "evidence": "",
            }
    return {"scope": scope, "answers": answers}


def validate_assessment(framework: Dict[str, Any], assessment: Dict[str, Any]) -> List[str]:
    """Return a list of problems with an assessment (empty if fine)."""
    problems: List[str] = []
    by_id = controls_by_id(framework)
    mode = assessment["scope"].get("mode")
    if mode not in MODES:
        problems.append(f"scope.mode must be one of {MODES}, got {mode!r}")
        mode = "both"
    for cid, entry in assessment["answers"].items():
        control = by_id.get(cid)
        if control is None:
            problems.append(f"{cid}: not a control in this framework version")
            continue
        ans = entry["answer"]
        if ans == "":
            continue
        if ans not in ANSWERS:
            problems.append(f"{cid}: answer {ans!r} is not one of {', '.join(ANSWERS)}")
            continue
        if ans != "na" and GUARANTEE_RANK[ans] > GUARANTEE_RANK[control["max_guarantee"]]:
            problems.append(
                f"{cid}: {ans!r} exceeds the strongest guarantee this control can give "
                f"({control['max_guarantee']}); choose {control['max_guarantee']} or lower"
            )
        if not applies(control, mode):
            problems.append(f"{cid}: not applicable to mode {mode!r} (answer ignored)")
    return problems


# ---------------------------------------------------------------- scoring


def compute(
    framework: Dict[str, Any], assessment: Dict[str, Any], strict: bool = False
) -> Dict[str, Any]:
    """Score an assessment.

    Unanswered controls are left out of the score and reported as lower coverage,
    unless ``strict`` is true, in which case they count as ``none``.
    """
    scope = assessment["scope"]
    mode = scope.get("mode", "both")
    answers = assessment["answers"]
    rows: List[Dict[str, Any]] = []

    for control in framework["controls"]:
        if not applies(control, mode):
            continue
        entry = answers.get(control["id"], {"answer": "", "note": "", "evidence": ""})
        ans = entry["answer"]
        target = GUARANTEE_RANK[control["max_guarantee"]]
        weight = SEVERITY_WEIGHT[control["severity"]]
        row = {
            "id": control["id"],
            "layer": control["layer"],
            "title": control["title"],
            "severity": control["severity"],
            "effort": control["effort"],
            "quick_win": bool(control["quick_win"]),
            "max_guarantee": control["max_guarantee"],
            "target": target,
            "answer": ans,
            "note": entry["note"],
            "evidence": entry["evidence"],
            "weight": weight,
            "level": None,
            "score": None,
            "status": "unanswered",
            "capped": False,
            "unevidenced": False,
        }
        if ans == "na":
            row["status"] = "na"
        else:
            if ans == "" and strict:
                ans = "none"
                row["answer"] = "none"
            if ans in GUARANTEE_RANK:
                level = GUARANTEE_RANK[ans]
                if level > target:
                    level = target
                    row["capped"] = True
                row["level"] = level
                row["score"] = level / target
                row["status"] = "scored"
                if level >= 2 and not entry["note"].strip() and not entry["evidence"].strip():
                    row["unevidenced"] = True
        rows.append(row)

    layers_out = []
    for layer in framework["layers"]:
        lrows = [r for r in rows if r["layer"] == layer["id"]]
        layers_out.append(_summarize_layer(layer, lrows))

    verbs_out = []
    for verb, info in framework["verbs"].items():
        vrows = [r for r in rows if _verb_of(framework, r["layer"]) == verb]
        verbs_out.append(_summarize_verb(verb, info, vrows))

    scored = [r for r in rows if r["status"] == "scored"]
    overall_score = _weighted(scored)
    overall = {
        "score": pct(overall_score) if overall_score is not None else None,
    }
    overall["band"] = band_for(overall["score"])

    applicable = [r for r in rows if r["status"] != "na"]
    coverage = {
        "applicable": len(applicable),
        "answered": len([r for r in applicable if r["status"] == "scored"]),
        "not_applicable": len([r for r in rows if r["status"] == "na"]),
        "total_in_mode": len(rows),
    }
    coverage["percent"] = (
        pct(coverage["answered"] / coverage["applicable"]) if coverage["applicable"] else None
    )

    return {
        "framework_version": framework["version"],
        "scope": scope,
        "strict": strict,
        "coverage": coverage,
        "overall": overall,
        "layers": layers_out,
        "verbs": verbs_out,
        "controls": rows,
        "unevidenced": [r["id"] for r in rows if r["unevidenced"]],
        "capped": [r["id"] for r in rows if r["capped"]],
    }


def _verb_of(framework: Dict[str, Any], layer_id: str) -> str:
    for layer in framework["layers"]:
        if layer["id"] == layer_id:
            return layer["verb"]
    raise KeyError(layer_id)


def _weighted(rows: List[Dict[str, Any]]) -> Optional[float]:
    total = sum(r["weight"] for r in rows)
    if not total:
        return None
    return sum(r["weight"] * r["score"] for r in rows) / total


def _counts(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"structural": 0, "procedural": 0, "guided": 0, "none": 0, "unanswered": 0, "na": 0}
    for r in rows:
        if r["status"] == "scored":
            counts[RANK_NAME[r["level"]]] += 1
        elif r["status"] == "na":
            counts["na"] += 1
        else:
            counts["unanswered"] += 1
    return counts


def _summarize_layer(layer: Dict[str, Any], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    scored = [r for r in rows if r["status"] == "scored"]
    s = _weighted(scored)
    return {
        "id": layer["id"],
        "number": layer["number"],
        "name": layer["name"],
        "verb": layer["verb"],
        "tagline": layer["tagline"],
        "score": pct(s) if s is not None else None,
        "total": len([r for r in rows if r["status"] != "na"]),
        "answered": len(scored),
        "counts": _counts(rows),
    }


def _summarize_verb(verb: str, info: Dict[str, Any], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    scored = [r for r in rows if r["status"] == "scored"]
    s = _weighted(scored)
    if s is None:
        status = "unassessed"
    else:
        weak_critical = any(r["severity"] == "critical" and r["score"] < 0.5 for r in scored)
        if s >= 0.8 and not weak_critical:
            status = "supported"
        elif s >= 0.4:
            status = "partly"
        else:
            status = "not_yet"
    return {
        "verb": verb,
        "label": info["label"],
        "score": pct(s) if s is not None else None,
        "status": status,
        "clause": VERB_CLAUSES[verb],
    }


# ---------------------------------------------------------------- action plan


def make_plan(result: Dict[str, Any]) -> Dict[str, Any]:
    """Turn a scored result into a prioritized, horizon-based action plan."""
    items = []
    for r in result["controls"]:
        if r["status"] == "na":
            continue
        if r["status"] == "scored" and r["score"] >= 1:
            continue
        unanswered = r["status"] == "unanswered"
        score = 0.0 if unanswered else r["score"]
        level = None if unanswered else r["level"]
        priority = r["weight"] * (1 - score) / EFFORT_COST[r["effort"]]
        items.append(
            {
                "id": r["id"],
                "title": r["title"],
                "severity": r["severity"],
                "effort": r["effort"],
                "quick_win": r["quick_win"],
                "current": "unanswered" if unanswered else RANK_NAME[level],
                "target": RANK_NAME[r["target"]],
                "next": None if unanswered else RANK_NAME[min(level + 1, r["target"])],
                "priority": r4(priority),
                "assess_first": unanswered,
            }
        )
    items.sort(key=lambda i: (-i["priority"], i["id"]))
    horizons = {
        "quick": [i for i in items if i["effort"] == "low"],
        "next": [i for i in items if i["effort"] == "medium"],
        "later": [i for i in items if i["effort"] == "high"],
    }
    critical = [i for i in items if i["severity"] == "critical"]
    critical.sort(key=lambda i: (-(1 if i["current"] in ("none", "unanswered") else 0), i["id"]))
    return {"critical": critical, "horizons": horizons, "count": len(items)}


# ---------------------------------------------------------------- progress


def compare(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two scored results of the same framework."""
    old_rows = {r["id"]: r for r in old["controls"]}
    new_rows = {r["id"]: r for r in new["controls"]}
    improved, regressed, added, removed = [], [], [], []
    for cid, nr in new_rows.items():
        orow = old_rows.get(cid)
        if orow is None:
            added.append(cid)
            continue
        o = -1 if orow["level"] is None else orow["level"]
        n = -1 if nr["level"] is None else nr["level"]
        if n > o:
            improved.append({"id": cid, "title": nr["title"], "from": orow["answer"] or "unanswered", "to": nr["answer"] or "unanswered"})
        elif n < o:
            regressed.append({"id": cid, "title": nr["title"], "from": orow["answer"] or "unanswered", "to": nr["answer"] or "unanswered"})
    for cid in old_rows:
        if cid not in new_rows:
            removed.append(cid)
    old_layers = {layer["id"]: layer for layer in old["layers"]}
    layer_deltas = []
    for layer in new["layers"]:
        o = old_layers.get(layer["id"])
        before = o["score"] if o else None
        after = layer["score"]
        delta = None if before is None or after is None else round(after - before, 1)
        layer_deltas.append({"id": layer["id"], "name": layer["name"], "before": before, "after": after, "delta": delta})
    b, a = old["overall"]["score"], new["overall"]["score"]
    return {
        "overall": {"before": b, "after": a, "delta": None if b is None or a is None else round(a - b, 1)},
        "layers": layer_deltas,
        "improved": improved,
        "regressed": regressed,
        "added": added,
        "removed": removed,
    }
