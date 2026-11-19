"""Load and validate the safeAI framework definition."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

GUARANTEE_RANK = {"none": 0, "guided": 1, "procedural": 2, "structural": 3}
RANK_NAME = {v: k for k, v in GUARANTEE_RANK.items()}
ANSWERS = ("none", "guided", "procedural", "structural", "na")
SEVERITY_WEIGHT = {"critical": 3, "high": 2, "medium": 1}
EFFORT_COST = {"low": 1, "medium": 2, "high": 3}
# A floor control is met at this level or above (2 = procedural).
FLOOR_MIN_LEVEL = 2
MODES = ("organization", "product", "both")
AUDIENCES = ("organization", "product")

REQUIRED_CONTROL_FIELDS = (
    "id",
    "layer",
    "title",
    "question",
    "audience",
    "max_guarantee",
    "severity",
    "effort",
    "quick_win",
    "steps",
    "evidence",
)


class FrameworkError(ValueError):
    """Raised when the framework file is invalid."""


def default_path() -> Path:
    return Path(__file__).parent / "data" / "safeai-framework.yaml"


def validate_framework(data: Dict[str, Any]) -> List[str]:
    """Return a list of problems (empty if the framework is valid)."""
    errors: List[str] = []
    for key in ("version", "guarantee_types", "verbs", "layers", "controls"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if errors:
        return errors

    layer_ids = [layer["id"] for layer in data["layers"]]
    if len(layer_ids) != len(set(layer_ids)):
        errors.append("duplicate layer ids")
    if len(layer_ids) != 7:
        errors.append(f"expected 7 layers, found {len(layer_ids)}")
    for layer in data["layers"]:
        if layer.get("verb") not in data["verbs"]:
            errors.append(f"layer {layer.get('id')}: unknown verb {layer.get('verb')!r}")
        for field in ("number", "name", "tagline", "question", "harm"):
            if field not in layer:
                errors.append(f"layer {layer.get('id')}: missing {field}")

    seen = set()
    for control in data["controls"]:
        cid = control.get("id", "<no id>")
        for field in REQUIRED_CONTROL_FIELDS:
            if field not in control:
                errors.append(f"{cid}: missing field {field}")
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen.add(cid)
        if control.get("layer") not in layer_ids:
            errors.append(f"{cid}: unknown layer {control.get('layer')!r}")
        elif not str(cid).startswith(control["layer"] + "."):
            errors.append(f"{cid}: id must start with its layer id")
        if control.get("max_guarantee") not in ("guided", "procedural", "structural"):
            errors.append(f"{cid}: bad max_guarantee {control.get('max_guarantee')!r}")
        if control.get("severity") not in SEVERITY_WEIGHT:
            errors.append(f"{cid}: bad severity {control.get('severity')!r}")
        if control.get("effort") not in EFFORT_COST:
            errors.append(f"{cid}: bad effort {control.get('effort')!r}")
        aud = control.get("audience")
        if not isinstance(aud, list) or not aud or any(a not in AUDIENCES for a in aud):
            errors.append(f"{cid}: audience must be a non-empty list of {AUDIENCES}")
        if control.get("quick_win") and control.get("effort") != "low":
            errors.append(f"{cid}: quick_win requires effort: low")
        if not control.get("steps"):
            errors.append(f"{cid}: needs at least one step")
        if "floor" in control and not isinstance(control["floor"], bool):
            errors.append(f"{cid}: floor must be true or false")
        if control.get("floor"):
            if control.get("max_guarantee") not in ("procedural", "structural"):
                errors.append(f"{cid}: a floor control must allow at least a procedural guarantee")
            if not str(control.get("floor_principle") or "").strip():
                errors.append(f"{cid}: a floor control needs a floor_principle")
    for layer_id in layer_ids:
        if not any(c.get("layer") == layer_id for c in data["controls"]):
            errors.append(f"layer {layer_id} has no controls")
    return errors


def load_framework(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load, validate, and return the framework as a dict."""
    p = Path(path) if path else default_path()
    try:
        with open(p, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise FrameworkError(f"{p} is not valid YAML: {exc}") from exc
    errors = validate_framework(data)
    if errors:
        raise FrameworkError("invalid framework file:\n  " + "\n  ".join(errors))
    return data


def applies(control: Dict[str, Any], mode: str) -> bool:
    """True if a control is in scope for the chosen assessment mode."""
    return mode == "both" or mode in control["audience"]


def controls_by_id(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {c["id"]: c for c in data["controls"]}


def layers_by_id(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {layer["id"]: layer for layer in data["layers"]}
