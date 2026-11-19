import re
from pathlib import Path

from safeai.cli import main
from safeai.framework import load_framework
from test_framework import FORBIDDEN
from safeai.vendor import load_questionnaire, to_markdown, validate_questionnaire

ROOT = Path(__file__).resolve().parent.parent


def test_questionnaire_is_valid_against_framework():
    assert validate_questionnaire(load_questionnaire(), load_framework()) == []


def test_validation_catches_unknown_control():
    data = load_questionnaire()
    data["questions"][0]["controls"] = ["L9.99"]
    assert any("L9.99" in p for p in validate_questionnaire(data, load_framework()))


def test_every_vendor_relevant_level_is_covered():
    covered = {c.split(".")[0] for q in load_questionnaire()["questions"] for c in q["controls"]}
    assert {"L1", "L2", "L3", "L4", "L6", "L7"} <= covered


def test_floor_controls_that_vendors_touch_are_asked_about():
    fw = load_framework()
    floor_ids = {c["id"] for c in fw["controls"] if c.get("floor")}
    asked = {c for q in load_questionnaire()["questions"] for c in q["controls"]}
    assert {"L3.04", "L4.03", "L4.07", "L4.09", "L4.11", "L4.12", "L6.02", "L7.09"} <= asked
    assert asked & floor_ids


def test_markdown_renders_every_question():
    data = load_questionnaire()
    md = to_markdown(data, "Example vendor")
    assert "Example vendor" in md
    for q in data["questions"]:
        assert f"### {q['id']}." in md


def test_questionnaire_is_generic():
    text = (ROOT / "src/safeai/data/vendor-questionnaire.yaml").read_text(encoding="utf-8").lower()
    for word in FORBIDDEN:
        assert not re.search(r"\b" + re.escape(word) + r"\b", text), word


def test_cli_writes_file(tmp_path):
    out = tmp_path / "q.md"
    assert main(["vendor-questions", "--vendor", "Example", "-o", str(out)]) == 0
    assert "V01." in out.read_text(encoding="utf-8")


def test_templates_cite_real_controls_and_cover_the_floor():
    fw = load_framework()
    ids = {c["id"] for c in fw["controls"]}
    for name in ("ai-use-policy.md", "ai-incident-response.md"):
        text = (ROOT / "templates" / name).read_text(encoding="utf-8")
        cited = set(re.findall(r"\bL[1-7]\.\d\d\b", text))
        assert cited, name
        assert cited <= ids, (name, cited - ids)
    policy = (ROOT / "templates" / "ai-use-policy.md").read_text(encoding="utf-8")
    floor_org = {c["id"] for c in fw["controls"] if c.get("floor") and "organization" in c["audience"]}
    for cid in floor_org:
        assert cid in policy, cid


def test_templates_do_not_state_legal_deadlines():
    text = (ROOT / "templates" / "ai-incident-response.md").read_text(encoding="utf-8")
    assert not re.search(r"\b\d+\s*(hours?|days?)\b", text)
