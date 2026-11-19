# Contributing to safeAI

Thank you for helping non-profits use AI more safely. The most valuable contributions are the ones that make a control clearer, more accurate, or easier for a small organization to act on.

## What to contribute

- **Control wording.** Questions must be answerable by a non-technologist. If you needed to explain a question to a colleague, rewrite it.
- **Steps and evidence.** Concrete, realistic actions that close a gap, and what someone could look at to confirm it.
- **Corrections.** If a control is wrong, outdated, or misleading, open an issue or a pull request.
- **Translations and accessibility fixes** for the browser tool and documents.
- **Examples.** Fictional ones only. Never contribute a real organization's assessment.

## How the framework is organized

`src/safeai/data/safeai-framework.yaml` is the single source of truth for both the command-line tool and the browser tool. Change controls there, not in the code.

Rules for controls:

1. **Ids are permanent.** Never reuse or renumber an `L<layer>.<nn>` id. Retire a control by marking it deprecated in the description, not by deleting its id.
2. **Set `max_guarantee` honestly.** If a control can only ever be guided (for example, "the AI reflects our mission"), do not label it structural.
3. **Floors, never doctrine.** The framework sets floors for safeguarding, data protection, and accountability. It must not tell any organization what its mission, faith, politics, or values should be. Level 5 asks whether an organization has written its own values down and checks the AI against them. It never supplies them.
4. **Stay generic.** No product names, vendor endorsements, or sector-specific or denomination-specific framing. A test enforces a list of forbidden names.
5. **No invented sources.** Cite only standards, laws, and documents you have checked exist and say what you claim. Mark anything unverified as such.
6. **Do not overclaim.** Nothing in this project promises that an AI system is "safe". Do not add language that implies certification or compliance.

## Development

```bash
pip install -e ".[dev]"
pytest                          # all tests must pass
python scripts/build_web.py     # rebuild web/index.html after changing the framework, scoring.js, or the template
```

The test suite checks that the browser and Python scorers produce identical results, so change `scoring.js` and `scoring.py` together.

## Pull requests

Keep changes focused, explain *why* in the description, and say how you checked them. By contributing you agree that your contribution is licensed under the Apache License 2.0, the same as the project.

## Conduct

Be kind and assume good faith. Many contributors are volunteers at small organizations. Critique the work, not the person.
