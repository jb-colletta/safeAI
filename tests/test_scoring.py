from pathlib import Path

from safeai.assessment import load_assessment, make_template
from safeai.framework import load_framework
from safeai.scoring import compare, compute, make_plan, normalize_assessment, validate_assessment

ROOT = Path(__file__).resolve().parent.parent
FW = load_framework()


def assess(mode="both", **answers):
    raw = {"scope": {"mode": mode}, "answers": answers}
    return normalize_assessment(raw)


def test_all_structural_scores_100_and_no_plan():
    answers = {c["id"]: c["max_guarantee"] for c in FW["controls"]}
    r = compute(FW, assess(**answers))
    assert r["overall"]["score"] == 100.0
    assert r["overall"]["band"] == "Leading"
    assert make_plan(r)["count"] == 0


def test_all_none_scores_zero_and_everything_in_plan():
    answers = {c["id"]: "none" for c in FW["controls"]}
    r = compute(FW, assess(**answers))
    assert r["overall"]["score"] == 0.0
    assert r["overall"]["band"] == "Exposed"
    assert make_plan(r)["count"] == len(FW["controls"])


def test_guided_is_full_credit_when_guided_is_the_ceiling():
    guided_max = next(c for c in FW["controls"] if c["max_guarantee"] == "guided")
    r = compute(FW, assess(**{guided_max["id"]: "guided"}))
    assert r["overall"]["score"] == 100.0


def test_partial_credit_fraction():
    c = next(c for c in FW["controls"] if c["max_guarantee"] == "structural")
    r = compute(FW, assess(**{c["id"]: "procedural"}))
    assert r["overall"]["score"] == 66.7


def test_exceeding_ceiling_is_flagged_and_capped():
    c = next(c for c in FW["controls"] if c["max_guarantee"] == "guided")
    a = assess(**{c["id"]: "structural"})
    assert any("exceeds" in p for p in validate_assessment(FW, a))
    r = compute(FW, a)
    assert r["capped"] == [c["id"]]
    assert r["overall"]["score"] == 100.0


def test_unanswered_excluded_unless_strict():
    r = compute(FW, assess(**{"L1.01": "procedural"}))
    assert r["overall"]["score"] == 100.0 and r["coverage"]["answered"] == 1
    s = compute(FW, assess(**{"L1.01": "procedural"}), strict=True)
    assert s["overall"]["score"] < 10 and s["coverage"]["answered"] == s["coverage"]["applicable"]


def test_not_applicable_excluded():
    r = compute(FW, assess(**{"L1.01": "na", "L1.02": "structural"}))
    assert r["overall"]["score"] == 100.0
    assert r["coverage"]["not_applicable"] == 1


def test_mode_filters_controls():
    org = compute(FW, assess("organization"))
    prod = compute(FW, assess("product"))
    both = compute(FW, assess("both"))
    assert len(org["controls"]) < len(both["controls"])
    assert len(prod["controls"]) < len(both["controls"])
    assert all("organization" in c["audience"] for c in FW["controls"] if c["id"] in {r["id"] for r in org["controls"]})


def test_unevidenced_claims_flagged():
    r = compute(FW, assess(**{"L1.02": "structural"}))
    assert r["unevidenced"] == ["L1.02"]
    a = normalize_assessment({"answers": {"L1.02": {"answer": "structural", "evidence": "config.png"}}})
    assert compute(FW, a)["unevidenced"] == []


def test_verb_status_requires_no_weak_critical():
    # Everything structural except one critical SEE control left at none.
    answers = {c["id"]: c["max_guarantee"] for c in FW["controls"]}
    answers["L1.02"] = "none"
    r = compute(FW, assess(**answers))
    see = next(v for v in r["verbs"] if v["verb"] == "SEE")
    assert see["status"] == "partly"


def test_plan_orders_by_value_for_effort_and_surfaces_critical():
    r = compute(FW, assess(**{c["id"]: "none" for c in FW["controls"]}))
    plan = make_plan(r)
    assert all(i["severity"] == "critical" for i in plan["critical"])
    pri = [i["priority"] for i in plan["horizons"]["quick"]]
    assert pri == sorted(pri, reverse=True)


def test_diff_detects_progress_and_regression():
    before = compute(FW, assess(**{"L1.01": "none", "L1.02": "structural"}))
    after = compute(FW, assess(**{"L1.01": "procedural", "L1.02": "guided"}))
    d = compare(before, after)
    assert [i["id"] for i in d["improved"]] == ["L1.01"]
    assert [i["id"] for i in d["regressed"]] == ["L1.02"]


def test_template_roundtrip_is_valid_and_blank():
    text = make_template(FW, mode="both", name="Test")
    p = ROOT / "tests" / "_tmp_template.yaml"
    p.write_text(text)
    try:
        a = load_assessment(p)
    finally:
        p.unlink()
    assert validate_assessment(FW, a) == []
    assert compute(FW, a)["coverage"]["answered"] == 0


def test_example_assessment_is_valid():
    a = load_assessment(ROOT / "examples" / "assessment.example.yaml")
    assert validate_assessment(FW, a) == []
    assert compute(FW, a)["overall"]["score"] is not None


# ---------------------------------------------------------------- human-dignity floor

FLOOR_IDS = [c["id"] for c in FW["controls"] if c.get("floor")]


def all_at_max(**overrides):
    answers = {c["id"]: c["max_guarantee"] for c in FW["controls"]}
    answers.update(overrides)
    return assess(**answers)


def test_floor_has_expected_shape():
    assert len(FLOOR_IDS) == 11
    for c in FW["controls"]:
        if c.get("floor"):
            assert c["max_guarantee"] in ("procedural", "structural"), c["id"]
            assert c["floor_principle"].strip(), c["id"]


def test_floor_met_when_everything_in_place():
    r = compute(FW, all_at_max())
    assert r["floor"]["status"] == "met"
    assert r["overall"]["gated"] is False
    assert r["overall"]["band"] == "Leading"


def test_floor_gap_holds_a_high_score_at_developing():
    r = compute(FW, all_at_max(**{"L4.07": "none"}))
    assert r["overall"]["score"] > 90          # the rest is excellent...
    assert r["overall"]["ungated_band"] == "Leading"
    assert r["overall"]["band"] == "Developing"  # ...but the floor holds the rating down
    assert r["overall"]["gated"] is True
    assert r["floor"]["status"] == "not_met"
    assert r["floor"]["not_met"] == ["L4.07"]


def test_guided_does_not_meet_the_floor_but_procedural_does():
    assert compute(FW, all_at_max(**{"L7.09": "guided"}))["floor"]["status"] == "not_met"
    assert compute(FW, all_at_max(**{"L7.09": "procedural"}))["floor"]["status"] == "met"


def test_unanswered_floor_control_is_unconfirmed_and_still_gates():
    answers = {c["id"]: c["max_guarantee"] for c in FW["controls"] if c["id"] != "L7.09"}
    r = compute(FW, assess(**answers))
    assert r["floor"]["status"] == "unconfirmed"
    assert r["floor"]["unconfirmed"] == ["L7.09"]
    assert r["overall"]["gated"] is True


def test_strict_mode_turns_unanswered_floor_control_into_not_met():
    answers = {c["id"]: c["max_guarantee"] for c in FW["controls"] if c["id"] != "L7.09"}
    r = compute(FW, assess(**answers), strict=True)
    assert r["floor"]["status"] == "not_met"


def test_not_applicable_floor_control_is_allowed_but_listed():
    r = compute(FW, all_at_max(**{"L4.04": "na"}))
    assert r["floor"]["status"] == "met"
    assert r["floor"]["not_applicable"] == ["L4.04"]


def test_floor_respects_mode():
    r = compute(FW, normalize_assessment(
        {"scope": {"mode": "organization"}, "answers": {c["id"]: c["max_guarantee"] for c in FW["controls"]}}))
    ids = [i["id"] for i in r["floor"]["controls"]]
    assert "L4.11" not in ids  # product-only control


def test_no_gate_when_nothing_answered():
    r = compute(FW, assess())
    assert r["overall"]["band"] is None
    assert r["overall"]["gated"] is False


def test_plan_lists_floor_gaps_first():
    r = compute(FW, all_at_max(**{"L4.07": "none", "L6.03": "guided"}))
    plan = make_plan(r)
    assert [i["id"] for i in plan["floor"]] == ["L4.07", "L6.03"]


def test_report_states_the_gate_plainly():
    from safeai.report import to_markdown
    r = compute(FW, all_at_max(**{"L4.07": "none"}))
    md = to_markdown(r, make_plan(r), FW)
    assert "Held at Developing" in md
    assert "## The human-dignity floor" in md
    assert "not a certification" in to_markdown(compute(FW, all_at_max()), make_plan(compute(FW, all_at_max())), FW)


def test_compare_reports_floor_change():
    before = compute(FW, all_at_max(**{"L4.07": "none"}))
    after = compute(FW, all_at_max())
    assert compare(before, after)["floor"] == {"before": "not_met", "after": "met"}
