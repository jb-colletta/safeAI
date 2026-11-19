# Using safeAI

## Before you start

- **Who should answer.** One person can start, but the answers are better when several people contribute: whoever manages your systems, your safeguarding or program lead, and someone from leadership. Expect 60 to 90 minutes for a first pass.
- **What to have in mind.** Which AI tools staff use (including AI built into software you already have), which systems any AI can connect to, and who owns each.
- **Pick a mode.**
  - *Organization*: you use AI tools and configure AI features in systems you run.
  - *Product*: you build software or integrations that include AI.
  - *Both*: you do both.

## In the browser

1. Open `web/index.html`. Fill in the name and mode.
2. On **Assess**, go through the seven levels. For each control choose the strongest statement that is true *today*. Open "Note and evidence" to record what supports your answer.
3. On **Results**, read the honest statements for SEE, DO, SAY, ANSWER and the level-by-level view.
4. On **Action plan**, start with critical gaps and the quick wins. Tick items off as you complete them.
5. **Download report (.md)** to share or file, **Save assessment (.json)** to continue later or track over time, or **Print or save as PDF**.

Answers are saved in your browser's local storage so a refresh does not lose them. Local storage can be cleared or unavailable (for example in a private window), so save the `.json` file when you finish.

## On the command line

```bash
safeai init --mode organization --name "My Org" -o assessment.yaml
```

Edit the file. Each control has a short comment with its question; set `answer:` to `structural`, `procedural`, `guided`, `none`, or `na`, and add a `note` and `evidence`.

```bash
safeai check  assessment.yaml     # validates answers, shows coverage
safeai report assessment.yaml -o report.md
safeai report assessment.yaml -f html -o report.html
safeai plan   assessment.yaml -o plan.md
safeai report assessment.yaml --strict      # count unanswered as "none"
safeai controls --layer 4 --mode organization   # browse the controls
```

### Track progress in git

Keep one assessment file per review, for example `assessments/2026-q1.yaml` and `assessments/2026-q3.yaml`, then:

```bash
safeai diff assessments/2026-q1.yaml assessments/2026-q3.yaml
```

shows the score change by level, gaps closed, and regressions.

### Run it in CI

A check that your assessment file stays valid:

```yaml
# .github/workflows/safeai.yml (in your own repository)
name: safeai
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pyyaml
      - run: pip install git+https://github.com/jb-colletta/safeAI.git
      - run: safeai check assessments/current.yaml
```

(Verify the action versions and install command against current documentation before relying on them.)

## Tips for honest answers

- Choose the answer that is true **today**, not the one you are working toward.
- "Guided" is not a failure. It tells you where you are and what to strengthen.
- If you cannot say what a reviewer could look at to confirm an answer, it is probably one step weaker than you think.
- If the people affected by a control (for example, staff who must follow a guideline) disagree with your answer, trust them.
- Re-assess whenever a vendor, model, or use case changes (see L2.08).

## Sharing results

Use the "What you can honestly say" statements, and no stronger. See [honest-claims.md](honest-claims.md).
