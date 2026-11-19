"""The browser tool's scorer (web/scoring.js) must agree with the Python scorer."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from safeai.assessment import load_assessment
from safeai.framework import load_framework
from safeai.scoring import compute, make_plan

ROOT = Path(__file__).resolve().parent.parent
pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")

JS = r"""
const S = require(process.argv[2]);
const fs = require('fs');
const fw = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const text = fs.readFileSync(process.argv[4], 'utf8');
const strict = process.argv[5] === '1';
const a = S.parseAssessmentFile(text);
const r = S.compute(fw, a, strict);
console.log(JSON.stringify({result: r, plan: S.makePlan(r), assessment: a}));
"""


def run_js(tmp_path, assessment_path, strict):
    fw = load_framework()
    fw_json = tmp_path / "fw.json"
    fw_json.write_text(json.dumps(fw))
    runner = tmp_path / "run.js"
    runner.write_text(JS)
    out = subprocess.run(
        ["node", str(runner), str(ROOT / "web" / "scoring.js"), str(fw_json), str(assessment_path), "1" if strict else "0"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


@pytest.mark.parametrize("strict", [False, True])
def test_scores_and_plan_match_python(tmp_path, strict):
    path = ROOT / "examples" / "assessment.example.yaml"
    fw = load_framework()
    py_result = compute(fw, load_assessment(path), strict=strict)
    py_plan = make_plan(py_result)
    js = run_js(tmp_path, path, strict)
    assert js["result"]["overall"] == py_result["overall"]
    assert js["result"]["coverage"] == py_result["coverage"]
    assert js["result"]["layers"] == py_result["layers"]
    assert js["result"]["verbs"] == py_result["verbs"]
    assert js["result"]["unevidenced"] == py_result["unevidenced"]
    assert [i["id"] for i in js["plan"]["critical"]] == [i["id"] for i in py_plan["critical"]]
    for key in ("quick", "next", "later"):
        assert [i["id"] for i in js["plan"]["horizons"][key]] == [i["id"] for i in py_plan["horizons"][key]]


def test_mini_yaml_reader_matches_pyyaml(tmp_path):
    path = ROOT / "examples" / "assessment.example.yaml"
    py = load_assessment(path)
    js = run_js(tmp_path, path, False)["assessment"]
    assert js["answers"] == py["answers"]
    assert js["scope"] == py["scope"]


def test_built_page_is_current():
    import subprocess, sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_web

    assert (ROOT / "web" / "index.html").read_text(encoding="utf-8") == build_web.build(), \
        "web/index.html is stale: run `python scripts/build_web.py`"
