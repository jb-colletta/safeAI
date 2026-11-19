"""Create and read assessment files."""

from __future__ import annotations

import datetime
import textwrap
from pathlib import Path
from typing import Any, Dict

import yaml

from .framework import applies, layers_by_id
from .scoring import normalize_assessment

HEADER = """\
# safeAI assessment
#
# For each control below, set `answer:` to one of:
#   structural   enforced in code or configuration; it cannot happen whatever the AI does
#   procedural   it cannot happen without a named person's approval or a recorded process
#   guided       people or the AI are told what to do; nothing ensures it
#   none         no control exists yet
#   na           does not apply to you (explain in `note`)
# Leave `answer:` blank for controls you have not assessed yet.
#
# Be honest rather than flattering. "guided" is a perfectly good answer: it tells you
# where to improve. Use `evidence:` to name something a reviewer could look at.
"""


def make_template(framework: Dict[str, Any], mode: str = "both", name: str = "") -> str:
    """Return a commented YAML assessment template for the chosen mode."""
    layers = layers_by_id(framework)
    today = datetime.date.today().isoformat()
    out = [HEADER]
    out.append("safeai_assessment: 1")
    out.append(f'framework_version: "{framework["version"]}"')
    out.append("scope:")
    out.append(f"  name: {_q(name)}            # the organization, system, or product being assessed")
    out.append(f"  mode: {mode}                # organization | product | both")
    out.append('  assessor: ""')
    out.append(f'  date: "{today}"')
    out.append('  description: ""')
    out.append("answers:")
    current = None
    for control in framework["controls"]:
        if not applies(control, mode):
            continue
        if control["layer"] != current:
            current = control["layer"]
            layer = layers[current]
            out.append("")
            out.append(f"  # {'=' * 70}")
            out.append(f"  # Level {layer['number']}: {layer['name']} ({layer['verb']})")
            out.append(f"  # {layer['tagline']}")
            out.append(f"  # {'=' * 70}")
        out.append("")
        out.append(f"  # {control['title']}  [{control['severity']}; strongest possible: {control['max_guarantee']}]")
        for line in textwrap.wrap(control["question"], width=84):
            out.append(f"  #   {line}")
        out.append(f"  {control['id']}:")
        out.append("    answer:")
        out.append('    note: ""')
        out.append('    evidence: ""')
    return "\n".join(out) + "\n"


def _q(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_assessment(path: Path) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected a YAML mapping at the top level")
    return normalize_assessment(raw)
