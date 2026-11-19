# safeAI

**Levels of AI safety for all non-profit organizations.**

"Is it safe to use AI?" is really seven questions: about your people's data, about the AI company, about what the AI can do on its own, about children and people in crisis, about whether it will speak against your mission, about whether it will pose as a person, and about who answers for all of it.

safeAI is a free, open-source toolkit that helps any non-profit, or any software product serving non-profits, to:

1. **Assess** where you stand on each of the seven levels (about 70 concrete controls).
2. **See the gaps honestly**, including the difference between a protection that is *enforced* and one that is only *hoped for*.
3. **Close them**, with a prioritized action plan and concrete steps for every control.
4. **Show progress** over time.

It works for an organization that *uses* AI tools, for a team that *builds* AI features or integrations, or both.

## Try it in 5 minutes

**In your browser, nothing to install:** [open the tool](https://jb-colletta.github.io/safeAI/), or download [`web/index.html`](web/index.html) and double-click it. Your answers stay in your browser. Nothing is uploaded.

**From the command line** (Python 3.9+ and PyYAML):

```bash
pip install -e .                      # or: pip install pyyaml && export PYTHONPATH=src
safeai init --mode both --name "My Organization" -o assessment.yaml
# edit assessment.yaml: set `answer:` for each control
safeai check  assessment.yaml         # catch mistakes
safeai report assessment.yaml -o report.md      # also: -f html, -f json
safeai plan   assessment.yaml -o plan.md
safeai diff   assessment-2026-q1.yaml assessment-2026-q3.yaml   # progress
```

Files saved from the browser tool (`.json`) and files edited for the command line (`.yaml`) are interchangeable. See [`examples/`](examples) for a fictional filled-in assessment and its report.

## The seven levels

Four verbs frame them: what the AI can **SEE**, what it can **DO**, what it can **SAY**, and who **ANSWERS** for it.

| | Level | The question it answers |
|---|---|---|
| SEE | 1. Data protection | Can the AI see personal or sensitive information? Could it leak? |
| SEE | 2. Vendor and model trust | Which AI company and model? Do they keep or train on our data? |
| DO | 3. Delegation and authority | Can it change records, spend money, or message people on its own? |
| DO | 4. Protection of the vulnerable | What about children, survivors, clients in crisis, people who depend on us? |
| SAY | 5. Mission and values fidelity | Will it say something that contradicts our mission, commitments, or facts? |
| SAY | 6. The human boundary | Will it pretend to be a person, or stand in for someone whose role needs a human? |
| ANSWER | 7. Accountability and governance | Who is responsible? Can we see what it did, and can we stop it? |

## The idea that makes this different: three kinds of guarantee

Most safety checklists say "yes/no". safeAI asks *how* each protection is guaranteed, because a customer, funder, or regulator who discovers the difference on their own stops trusting everything else you told them.

| Guarantee | Meaning | Fails by |
|---|---|---|
| **Structural** | Enforced in code or configuration. It cannot happen, whatever the AI does or is told. | Misconfiguration; rules too narrow |
| **Procedural** | It cannot happen without a named person's approval or a recorded process. | Rubber-stamping; approval fatigue |
| **Guided** | People or the AI are told what to do. Nothing ensures it. | Drift, forgetfulness, prompt injection, model updates |

**The rule: never present a guided control as structural.** Guided controls are valuable, and much of what keeps an AI faithful to a mission will always be guided. But say so. The report turns your answers into statements you can honestly make (and flags claims that have no evidence behind them). See [docs/honest-claims.md](docs/honest-claims.md).

## A floor under everything: human dignity

Eleven of the controls form a **human-dignity floor**. They say that people, not algorithms, decide who receives help; that a person's worth is never scored by what they produce; that the AI never passes as a person or simulates care as a real relationship; that children and the vulnerable are protected by the provider, not left to families; and that someone identifiable answers for the AI and anyone affected can appeal to a human.

If the floor is not met, your overall rating is held at *Developing* however well the rest scores. Beyond the floor, your organization writes its own mission and values along the seven levels (Level 5). The floor can be raised but never lowered. See [docs/floor.md](docs/floor.md), including what it does *not* claim.

## Templates and vendor questions

- [`templates/ai-use-policy.md`](templates/ai-use-policy.md): a fill-in-the-blank AI use policy, one section per level. Each clause names its control and the kind of guarantee it can honestly be. Delete any clause you are not prepared to follow.
- [`templates/ai-incident-response.md`](templates/ai-incident-response.md): a one-to-two page note for when an AI does something it should not.
- `safeai vendor-questions -o questions.md`: the questions to send an AI vendor, each tied to the controls it helps you answer, with what a good answer and a worrying one look like.

These are starting points, not legal advice.

## Repository map

| Path | What it is |
|---|---|
| `src/safeai/data/safeai-framework.yaml` | The framework: levels, guarantee types, and every control. The single source of truth. |
| `src/safeai/` | Python package and `safeai` command |
| `web/` | Browser tool (`index.html` is built from `index.template.html` + `scoring.js` + the framework) |
| `templates/` | Fill-in-the-blank AI use policy and incident response note |
| `examples/` | A fictional assessment and its generated report |
| `docs/` | [Framework](docs/framework.md) · [Human-dignity floor](docs/floor.md) · [Using the tool](docs/using-the-tool.md) · [Scoring](docs/scoring.md) · [Honest claims](docs/honest-claims.md) · [Getting it reviewed](docs/expert-review.md) · [References](docs/references.md) · [Roadmap](docs/roadmap.md) |
| `tests/` | Unit tests, including a check that the browser and Python scorers agree |

## What this is not

- It is **not an audit, certification, or legal advice**. Scores come from self-reported answers and are indicative only.
- It does **not** make an AI system safe. It helps you find and close the gaps. Laws, funder rules, and professional standards vary by place and sector; check the ones that apply to you.
- It sets **floors for safeguarding and data protection, never doctrine**. Your mission and values are yours to write; the toolkit never supplies them.

## Contributing

Contributions that make the controls clearer, more accurate, or more useful to small organizations are very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). To report a security problem, see [SECURITY.md](SECURITY.md).

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
