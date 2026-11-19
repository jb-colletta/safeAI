# Changelog

All notable changes are listed here. Versions follow [Semantic Versioning](https://semver.org/).

## 0.1.0 (first release)

- Seven levels and 70 controls, each with a question, steps, evidence, severity, effort, and the highest honest guarantee type (structural, procedural, or guided).
- Human-dignity floor: 11 controls that hold the overall rating at *Developing* until they are met at procedural or structural level.
- Scoring, report, action plan, and progress comparison, in Python and in the browser, kept in agreement by tests.
- Command line: `init`, `check`, `report`, `plan`, `diff`, `controls`, `vendor-questions`, `framework-check`.
- Browser tool that makes no network calls, also published through GitHub Pages.
- Fill-in-the-blank AI use policy and AI incident response note in `templates/`.
- Questions to send an AI vendor, tied to controls.
- Fictional example assessment and report.

Known limits: no outside expert has reviewed the controls, and no organization has piloted the tool. See [docs/expert-review.md](docs/expert-review.md).
