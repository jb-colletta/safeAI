#!/usr/bin/env python3
"""Build web/index.html: one self-contained file with the framework and scoring inlined.

Run from the repository root after changing the framework data, web/scoring.js, or
web/index.template.html:

    python scripts/build_web.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from safeai.framework import load_framework  # noqa: E402


def build() -> str:
    framework = load_framework()
    template = (ROOT / "web" / "index.template.html").read_text(encoding="utf-8")
    scoring = (ROOT / "web" / "scoring.js").read_text(encoding="utf-8")
    # Keep "</script" sequences from ending the inline script early.
    fw_json = json.dumps(framework, ensure_ascii=False).replace("</", "<\\/")
    scoring = scoring.replace("</script", "<\\/script")
    for marker in ("/*__SCORING_JS__*/", "/*__FRAMEWORK_JSON__*/null"):
        if template.count(marker) != 1:
            raise SystemExit(f"template must contain {marker} exactly once")
    return template.replace("/*__SCORING_JS__*/", scoring).replace(
        "/*__FRAMEWORK_JSON__*/null", fw_json
    )


def main() -> int:
    out = ROOT / "web" / "index.html"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
