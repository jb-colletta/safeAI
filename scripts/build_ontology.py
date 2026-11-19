#!/usr/bin/env python3
"""Build web/safeai.ttl: the framework as an OWL ontology in Turtle.

The YAML framework stays the single source of truth. This file is generated from it,
so other tools (ontology editors, knowledge graphs, mapping projects) can refer to
levels and controls by stable IRIs. Do not edit web/safeai.ttl by hand.

Run from the repository root after changing the framework data:

    python scripts/build_ontology.py

The output is deterministic: the same framework always produces the same bytes, so CI
can check that the committed file is up to date. Only PyYAML is needed.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from safeai.framework import load_framework  # noqa: E402

# PROVISIONAL before version 1.0. Hash IRIs resolve to the published Turtle file on
# the GitHub Pages site for now. Before 1.0 (or before outside use, whichever comes
# first) this is expected to move to a permanent redirect service such as w3id.org.
# From 1.0 on, IRIs are permanent, like control ids.
BASE = "https://jb-colletta.github.io/safeAI/safeai.ttl"
NS = BASE + "#"

PREFIXES = [
    ("sai", NS),
    ("owl", "http://www.w3.org/2002/07/owl#"),
    ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
    ("xsd", "http://www.w3.org/2001/XMLSchema#"),
    ("skos", "http://www.w3.org/2004/02/skos/core#"),
    ("dcterms", "http://purl.org/dc/terms/"),
]


# ---------------------------------------------------------------- Turtle helpers

def lit(value: Any, lang: str = "en") -> str:
    """A Turtle string literal, escaped per the Turtle 1.1 grammar."""
    s = str(value)
    s = (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{s}"@{lang}' if lang else f'"{s}"'


def typed(value: Any, datatype: str) -> str:
    if datatype == "xsd:boolean":
        return f'"{"true" if value else "false"}"^^xsd:boolean'
    return f'"{value}"^^{datatype}'


def block(subject: str, pairs: Iterable[tuple]) -> str:
    """One Turtle subject block. Each pair is (predicate, object or list of objects)."""
    lines: List[str] = []
    for pred, obj in pairs:
        objs = obj if isinstance(obj, list) else [obj]
        objs = [o for o in objs if o is not None]
        if not objs:
            continue
        lines.append(f"    {pred} " + " ,\n        ".join(objs))
    return subject + "\n" + " ;\n".join(lines) + " .\n"


def term(prefix: str, value: str) -> str:
    """A local name for an enumerated value, e.g. term('effort', 'low') -> sai:effort-low."""
    return f"sai:{prefix}-{value}"


# ---------------------------------------------------------------- vocabulary (TBox)

CLASSES = [
    ("Verb", "Verb", "One of the four groups the seven levels fall into: SEE, DO, SAY, ANSWER."),
    ("Level", "Level", "One of the seven levels of the question \"Is it safe?\"."),
    ("Control", "Control", "An individual, assessable safeguard within one level."),
    ("FloorControl", "Human-dignity floor control",
     "A control in the human-dignity floor. It must be met at procedural or structural "
     "level, or the overall rating is held at Developing."),
    ("GuaranteeType", "Guarantee type",
     "How a control's protection is guaranteed: structural, procedural, guided, or none."),
    ("Audience", "Audience",
     "Who a control applies to: an organization that uses AI tools, or a product that builds AI features."),
    ("Severity", "Severity", "How bad a gap in a control is."),
    ("Effort", "Effort", "The rough cost of closing a gap in a control."),
]

# (name, label, domain, range, functional, comment)
OBJECT_PROPERTIES = [
    ("verb", "verb", "Level", "Verb", True, "The group a level belongs to."),
    ("level", "level", "Control", "Level", True, "The level a control belongs to."),
    ("maxGuarantee", "maximum guarantee", "Control", "GuaranteeType", True,
     "The strongest realistic guarantee for this control. Never present a guided control as structural."),
    ("audience", "audience", "Control", "Audience", False, "Who the control applies to."),
    ("severity", "severity", "Control", "Severity", True, "How bad a gap in this control is."),
    ("effort", "effort", "Control", "Effort", True, "The rough cost of closing a gap."),
]

# (name, label, domain, range, functional, comment)
DATATYPE_PROPERTIES = [
    ("number", "number", "Level", "xsd:integer", True, "The level's position, 1 to 7."),
    ("rank", "rank", "GuaranteeType", "xsd:integer", True,
     "Strength of a guarantee type: structural 3, procedural 2, guided 1, none 0."),
    ("quickWin", "quick win", "Control", "xsd:boolean", True,
     "True if a typical organization can close the gap in weeks."),
]

# Text fields are annotation properties, so reasoners ignore them and editors show them as notes.
ANNOTATION_PROPERTIES = [
    ("question", "question", "A self-assessment question a non-technologist can answer."),
    ("tagline", "tagline", "A one-line promise that a level makes."),
    ("harm", "harm", "The harm a level protects against."),
    ("summary", "summary", "A short description of a verb."),
    ("meaning", "meaning", "What a guarantee type means."),
    ("example", "example", "An example of a guarantee type."),
    ("failsBy", "fails by", "How a guarantee type typically fails."),
    ("step", "step",
     "A concrete action that closes a gap. Each value starts with its position (\"1. \"), "
     "because annotation values carry no order of their own."),
    ("evidence", "evidence", "Something an auditor could look at to confirm the answer."),
    ("floorPrinciple", "floor principle", "One plain sentence naming what a floor control protects."),
]


def tbox(version: str) -> List[str]:
    out: List[str] = []
    out.append(block(f"<{BASE}>", [
        ("a", "owl:Ontology"),
        ("owl:versionIRI", f"<https://jb-colletta.github.io/safeAI/safeai-{version}.ttl>"),
        ("owl:versionInfo", lit(version, lang="")),
        ("rdfs:label", lit("safeAI framework: seven levels of \"Is it safe?\"")),
        ("rdfs:comment", lit(
            "Levels, guarantee types, and controls for assessing gaps in safe AI use. "
            "Generated from src/safeai/data/safeai-framework.yaml, which is the source of truth. "
            "A planning aid based on self-reported answers, not an audit, certification, or legal advice. "
            "IRIs are provisional before version 1.0 and may change.")),
        ("dcterms:license", "<https://www.apache.org/licenses/LICENSE-2.0>"),
        ("dcterms:source", "<https://github.com/jb-colletta/safeAI>"),
    ]))
    out.append("# ---- Annotation properties from other vocabularies\n")
    for p in ("skos:notation", "skos:definition", "dcterms:license", "dcterms:source"):
        out.append(f"{p} a owl:AnnotationProperty .\n")
    out.append("\n# ---- Classes\n")
    for name, label, comment in CLASSES:
        pairs = [("a", "owl:Class"), ("rdfs:label", lit(label)), ("skos:definition", lit(comment))]
        if name == "FloorControl":
            pairs.insert(1, ("rdfs:subClassOf", "sai:Control"))
        out.append(block(f"sai:{name}", pairs))
    out.append("# ---- Object properties\n")
    for name, label, dom, rng, functional, comment in OBJECT_PROPERTIES:
        types = ["owl:ObjectProperty"] + (["owl:FunctionalProperty"] if functional else [])
        out.append(block(f"sai:{name}", [
            ("a", types), ("rdfs:label", lit(label)), ("rdfs:comment", lit(comment)),
            ("rdfs:domain", f"sai:{dom}"), ("rdfs:range", f"sai:{rng}"),
        ]))
    out.append("# ---- Datatype properties\n")
    for name, label, dom, rng, functional, comment in DATATYPE_PROPERTIES:
        types = ["owl:DatatypeProperty"] + (["owl:FunctionalProperty"] if functional else [])
        out.append(block(f"sai:{name}", [
            ("a", types), ("rdfs:label", lit(label)), ("rdfs:comment", lit(comment)),
            ("rdfs:domain", f"sai:{dom}"), ("rdfs:range", rng),
        ]))
    out.append("# ---- Annotation properties\n")
    for name, label, comment in ANNOTATION_PROPERTIES:
        out.append(block(f"sai:{name}", [
            ("a", "owl:AnnotationProperty"), ("rdfs:label", lit(label)), ("rdfs:comment", lit(comment)),
        ]))
    return out


# ---------------------------------------------------------------- individuals (ABox)

SEVERITIES = ("critical", "high", "medium")
EFFORTS = ("low", "medium", "high")
AUDIENCES = (
    ("organization", "Organization", "An organization that uses AI tools."),
    ("product", "Product", "A product or integration that builds AI features."),
)


def abox(fw: Dict[str, Any]) -> List[str]:
    out: List[str] = []

    out.append("# ---- Guarantee types\n")
    gt_names = []
    for key, g in sorted(fw["guarantee_types"].items(), key=lambda kv: -kv[1]["rank"]):
        gt_names.append(f"sai:{key}")
        out.append(block(f"sai:{key}", [
            ("a", ["owl:NamedIndividual", "sai:GuaranteeType"]),
            ("rdfs:label", lit(g["label"])),
            ("sai:rank", typed(g["rank"], "xsd:integer")),
            ("sai:meaning", lit(g["meaning"]) if g.get("meaning") else None),
            ("sai:example", lit(g["example"]) if g.get("example") else None),
            ("sai:failsBy", lit(g["fails_by"]) if g.get("fails_by") else None),
        ]))

    out.append("# ---- Audiences, severities, efforts\n")
    aud_names, sev_names, eff_names = [], [], []
    for key, label, comment in AUDIENCES:
        aud_names.append(term("audience", key))
        out.append(block(term("audience", key), [
            ("a", ["owl:NamedIndividual", "sai:Audience"]),
            ("rdfs:label", lit(label)), ("skos:definition", lit(comment)),
            ("skos:notation", lit(key, lang="")),
        ]))
    for key in SEVERITIES:
        sev_names.append(term("severity", key))
        out.append(block(term("severity", key), [
            ("a", ["owl:NamedIndividual", "sai:Severity"]),
            ("rdfs:label", lit(key.capitalize())), ("skos:notation", lit(key, lang="")),
        ]))
    for key in EFFORTS:
        eff_names.append(term("effort", key))
        out.append(block(term("effort", key), [
            ("a", ["owl:NamedIndividual", "sai:Effort"]),
            ("rdfs:label", lit(key.capitalize())), ("skos:notation", lit(key, lang="")),
        ]))

    out.append("# ---- Verbs\n")
    verb_names = []
    for key, v in fw["verbs"].items():
        verb_names.append(f"sai:{key}")
        out.append(block(f"sai:{key}", [
            ("a", ["owl:NamedIndividual", "sai:Verb"]),
            ("rdfs:label", lit(v["label"])),
            ("skos:notation", lit(key, lang="")),
            ("sai:summary", lit(v["summary"])),
        ]))

    out.append("# ---- Levels\n")
    level_names = []
    for layer in fw["layers"]:
        level_names.append(f"sai:{layer['id']}")
        out.append(block(f"sai:{layer['id']}", [
            ("a", ["owl:NamedIndividual", "sai:Level"]),
            ("rdfs:label", lit(f"Level {layer['number']}: {layer['name']}")),
            ("skos:notation", lit(layer["id"], lang="")),
            ("sai:number", typed(layer["number"], "xsd:integer")),
            ("sai:verb", f"sai:{layer['verb']}"),
            ("sai:tagline", lit(layer["tagline"])),
            ("sai:question", lit(layer["question"])),
            ("sai:harm", lit(layer["harm"])),
        ]))

    out.append("# ---- Controls\n")
    control_names = []
    for c in fw["controls"]:
        control_names.append(f"sai:{c['id']}")
        classes = ["owl:NamedIndividual", "sai:FloorControl" if c.get("floor") else "sai:Control"]
        out.append(block(f"sai:{c['id']}", [
            ("a", classes),
            ("rdfs:label", lit(c["title"])),
            ("skos:notation", lit(c["id"], lang="")),
            ("sai:level", f"sai:{c['layer']}"),
            ("sai:question", lit(c["question"])),
            ("sai:audience", [term("audience", a) for a in c["audience"]]),
            ("sai:maxGuarantee", f"sai:{c['max_guarantee']}"),
            ("sai:severity", term("severity", c["severity"])),
            ("sai:effort", term("effort", c["effort"])),
            ("sai:quickWin", typed(bool(c.get("quick_win")), "xsd:boolean")),
            ("sai:floorPrinciple", lit(c["floor_principle"]) if c.get("floor") else None),
            ("sai:step", [lit(f"{i}. {s}") for i, s in enumerate(c["steps"], 1)]),
            ("sai:evidence", [lit(e) for e in c.get("evidence") or []]),
        ]))

    # Unique-name assumption, stated explicitly so a reasoner can catch a control given
    # two different levels or two maximum guarantees.
    out.append("# ---- Distinct individuals\n")
    for group in (gt_names, aud_names, sev_names, eff_names, verb_names, level_names, control_names):
        out.append("[] a owl:AllDifferent ;\n    owl:distinctMembers ( " + " ".join(group) + " ) .\n")
    return out


def build() -> str:
    fw = load_framework()
    head = [
        "# GENERATED FILE. Do not edit by hand.",
        "# Source: src/safeai/data/safeai-framework.yaml",
        "# Rebuild: python scripts/build_ontology.py",
        "# SPDX-License-Identifier: Apache-2.0",
        "",
    ]
    head += [f"@prefix {p}: <{iri}> ." for p, iri in PREFIXES]
    body = tbox(fw["version"]) + abox(fw)
    return "\n".join(head) + "\n\n" + "\n".join(body)


def main() -> int:
    out = ROOT / "web" / "safeai.ttl"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
