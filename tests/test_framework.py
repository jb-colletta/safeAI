import re
from pathlib import Path

import pytest

from safeai.framework import FrameworkError, load_framework, validate_framework

ROOT = Path(__file__).resolve().parent.parent
# Names this project must stay free of: it is a generic toolkit for any organization.
FORBIDDEN = [
    "ministryplatform", "ministry platform", "realm", "acst", "mp-mcp", "dataguard",
    "deontic", "church", "diocese", "parish", "catholic", "protestant", "magnifica",
]


def test_framework_valid():
    fw = load_framework()
    assert len(fw["layers"]) == 7
    assert len(fw["controls"]) >= 60


def test_every_layer_has_controls_for_both_audiences():
    fw = load_framework()
    for layer in fw["layers"]:
        cs = [c for c in fw["controls"] if c["layer"] == layer["id"]]
        assert any("organization" in c["audience"] for c in cs), layer["id"]
        assert any("product" in c["audience"] for c in cs), layer["id"]


def test_validation_catches_problems():
    fw = load_framework()
    bad = {**fw, "controls": fw["controls"] + [dict(fw["controls"][0])]}
    assert any("duplicate" in e for e in validate_framework(bad))
    broken = dict(fw["controls"][0], severity="urgent")
    assert any("severity" in e for e in validate_framework({**fw, "controls": [broken] + fw["controls"][1:]}))
    with pytest.raises(FrameworkError):
        from safeai import framework as f
        f.load_framework(ROOT / "README.md")  # not YAML mapping with the right keys


def test_no_forbidden_references_in_repository():
    """The repo must not mention the example products or any faith-specific framing."""
    skip_dirs = {".git", "__pycache__", ".pytest_cache"}
    skip_files = {"CLAUDE.md", "test_framework.py"}
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or skip_dirs & set(path.parts) or path.name in skip_files:
            continue
        if path.suffix in {".png", ".jpg", ".pdf"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for word in FORBIDDEN:
            if re.search(r"\b" + re.escape(word) + r"\b", text):
                hits.append((str(path.relative_to(ROOT)), word))
    assert not hits, hits


def test_floor_validation_catches_problems():
    fw = load_framework()
    controls = [dict(c) for c in fw["controls"]]
    floor_ctrl = next(c for c in controls if c.get("floor"))
    floor_ctrl.pop("floor_principle")
    assert any("floor_principle" in e for e in validate_framework({**fw, "controls": controls}))
    controls = [dict(c) for c in fw["controls"]]
    guided = next(c for c in controls if c["max_guarantee"] == "guided")
    guided["floor"] = True
    guided["floor_principle"] = "x"
    assert any("procedural" in e for e in validate_framework({**fw, "controls": controls}))


def test_floor_principles_stay_generic():
    """Floor wording must stand on its own, with no source or tradition named."""
    fw = load_framework()
    for c in fw["controls"]:
        if c.get("floor"):
            text = (c["floor_principle"] + " " + c["title"]).lower()
            assert not re.search(r"encyclical|pope|scripture|doctrine|dogma", text), c["id"]
