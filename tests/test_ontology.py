"""web/safeai.ttl is generated from the framework and must stay in step with it."""

import importlib.util
import re
from pathlib import Path

import pytest

from safeai.framework import load_framework

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "web" / "safeai.ttl"
NS = "https://jb-colletta.github.io/safeAI/safeai.ttl#"


def _builder():
    spec = importlib.util.spec_from_file_location("build_ontology", ROOT / "scripts" / "build_ontology.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_committed_file_is_up_to_date():
    assert TTL.read_text(encoding="utf-8") == _builder().build(), (
        "web/safeai.ttl is out of date: run python scripts/build_ontology.py"
    )


def test_namespace_marked_provisional_before_1_0():
    """Until 1.0 the IRIs may move, and the ontology must say so."""
    fw = load_framework()
    if int(str(fw["version"]).split(".")[0]) < 1:
        assert "provisional before version 1.0" in TTL.read_text(encoding="utf-8")


def test_build_is_deterministic():
    b = _builder()
    assert b.build() == b.build()


def test_every_level_and_control_has_a_block():
    fw = load_framework()
    text = TTL.read_text(encoding="utf-8")
    for layer in fw["layers"]:
        assert re.search(rf"^sai:{re.escape(layer['id'])}\n    a owl:NamedIndividual", text, re.M), layer["id"]
    for c in fw["controls"]:
        assert re.search(rf"^sai:{re.escape(c['id'])}\n    a owl:NamedIndividual", text, re.M), c["id"]


def test_floor_controls_are_typed_as_floor():
    fw = load_framework()
    text = TTL.read_text(encoding="utf-8")
    floor_ids = {c["id"] for c in fw["controls"] if c.get("floor")}
    typed = set(re.findall(r"^sai:(L\d\.\d\d)\n    a owl:NamedIndividual ,\n        sai:FloorControl", text, re.M))
    assert typed == floor_ids
    assert text.count("sai:floorPrinciple ") == len(floor_ids)


def test_literal_escaping():
    lit = _builder().lit
    assert lit('a "b" \\ c\nd') == '"a \\"b\\" \\\\ c\\nd"@en'
    assert lit("x", lang="") == '"x"'


def test_prefixed_names_are_valid_turtle():
    """Local names must fit the Turtle PN_LOCAL rule (no trailing dot, safe characters)."""
    text = TTL.read_text(encoding="utf-8")
    # Strip string literals so their contents are not mistaken for names.
    code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    code = "\n".join(line for line in code.splitlines() if not line.startswith("@prefix"))
    names = re.findall(r"\bsai:([^\s;,.()\[\]]+(?:\.[^\s;,.()\[\]]+)*)", code)
    assert len(names) > 500
    for name in names:
        assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_\-]*(\.[A-Za-z0-9_\-]+)*", name), name


def test_parses_as_rdf_and_matches_framework():
    """A real parse. Runs in CI, where rdflib is a dev dependency; skipped if it is missing."""
    rdflib = pytest.importorskip("rdflib")
    from rdflib.namespace import OWL, RDF, RDFS

    g = rdflib.Graph()
    g.parse(TTL, format="turtle")
    sai = rdflib.Namespace(NS)
    fw = load_framework()

    controls = set(g.subjects(RDF.type, sai.Control)) | set(g.subjects(RDF.type, sai.FloorControl))
    assert len(controls) == len(fw["controls"])
    assert len(set(g.subjects(RDF.type, sai.FloorControl))) == sum(1 for c in fw["controls"] if c.get("floor"))
    assert (sai.FloorControl, RDFS.subClassOf, sai.Control) in g
    assert len(set(g.subjects(RDF.type, sai.Level))) == 7

    for c in fw["controls"]:
        s = sai[c["id"]]
        assert (s, sai.level, sai[c["layer"]]) in g
        assert (s, sai.maxGuarantee, sai[c["max_guarantee"]]) in g
        assert len(list(g.objects(s, sai.step))) == len(c["steps"])
        assert str(g.value(s, RDFS.label)) == c["title"]
    assert (rdflib.URIRef(NS[:-1]), RDF.type, OWL.Ontology) in g
