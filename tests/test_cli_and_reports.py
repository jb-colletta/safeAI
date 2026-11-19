from pathlib import Path

from safeai.cli import main

ROOT = Path(__file__).resolve().parent.parent
EX = str(ROOT / "examples" / "assessment.example.yaml")


def test_init_check_report_plan_diff(tmp_path, capsys):
    t = tmp_path / "a.yaml"
    assert main(["init", "--mode", "organization", "--name", "X", "-o", str(t)]) == 0
    assert main(["init", "-o", str(t)]) == 1  # refuses to overwrite
    assert main(["check", str(t)]) == 0
    for fmt in ("md", "html", "json"):
        out = tmp_path / f"r.{fmt}"
        assert main(["report", EX, "-f", fmt, "-o", str(out)]) == 0
        assert out.read_text()
    assert "<table>" in (tmp_path / "r.html").read_text()
    assert main(["plan", EX, "-o", str(tmp_path / "p.md")]) == 0
    assert main(["diff", EX, EX, "-o", str(tmp_path / "d.md")]) == 0
    assert main(["controls", "--layer", "4"]) == 0
    assert main(["framework-check"]) == 0


def test_check_reports_bad_answer(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text('scope:\n  mode: both\nanswers:\n  L1.01:\n    answer: maybe\n  L9.99:\n    answer: none\n')
    assert main(["check", str(bad)]) == 1


def test_report_has_honesty_sections():
    from safeai.assessment import load_assessment
    from safeai.framework import load_framework
    from safeai.report import to_markdown
    from safeai.scoring import compute, make_plan

    fw = load_framework()
    r = compute(fw, load_assessment(Path(EX)))
    md = to_markdown(r, make_plan(r), fw)
    for heading in ("What you can honestly say", "The seven levels", "Action plan", "Critical gaps first"):
        assert heading in md


def test_html_report_escapes_user_text(tmp_path):
    from safeai.report import to_html
    from safeai.framework import load_framework
    from safeai.scoring import compute, make_plan, normalize_assessment

    fw = load_framework()
    a = normalize_assessment({"scope": {"name": "<script>alert(1)</script>"}, "answers": {}})
    r = compute(fw, a)
    out = to_html(r, make_plan(r), fw)
    assert "<script>alert(1)</script>" not in out
