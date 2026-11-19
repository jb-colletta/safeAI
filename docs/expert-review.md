# Getting the framework reviewed

safeAI's controls were written and tested by its authors. They have **not** been reviewed by outside specialists. Until they are, say so (see [honest claims](honest-claims.md)). This page is a plan for getting that review, and for recording it honestly.

## Who to ask

Three reviewers cover most of the ground. Each needs about one to two hours.

| Reviewer | Background | Reads first |
|---|---|---|
| **Security and privacy** | Someone who secures systems or handles data protection for a living | Levels 1, 3 and 7 |
| **Safeguarding** | Someone who protects children or vulnerable adults in a program, school, clinic, or agency | Levels 4 and 6, and the [human-dignity floor](floor.md) |
| **Small-organization operator** | Someone who runs IT or operations at a small non-profit | A full pass in the browser tool, as if answering for their own organization |

A fourth, optional reviewer is a **lawyer** who knows your sector, to look at any control that depends on a law or contract (L1.08, L2.04, L6.02). The toolkit states no legal requirements, and a reviewer should confirm that it does not imply any.

Ask people in your own network first: a board member, a funder's technical contact, a peer organization, a local university or professional association. Many will do one short review as a favor. Do not pay for a review that you then describe as independent without saying so.

## What to send

1. The link to the repository and to [docs/framework.md](framework.md).
2. The control list for their levels: `safeai controls --layer 4`, or the browser tool's Assess tab.
3. [docs/floor.md](floor.md) and [docs/honest-claims.md](honest-claims.md).
4. The questions below, and a date by which a short reply is helpful.

Tell them plainly: this is a self-assessment aid, it is not an audit or a certification, and you are asking whether the guidance is accurate and useful, not for an endorsement.

## What to ask

For each control in their levels:

1. **Accurate?** Is the question and each step correct and safe to follow?
2. **Missing?** What common failure does the framework not mention?
3. **Weight?** Is the severity (critical, high, medium) and effort right?
4. **Honest kind?** Is the highest honest guarantee type right (structural, procedural, guided)? Could a control really be structural, or does it always depend on a person or on the AI following instructions?
5. **Clear?** Would a non-specialist at a small organization understand it and know what to do next?
6. **Harm?** Is there any step that could make things worse if followed literally?

And overall:

- Is anything in the floor set too strict, too loose, or in the wrong place?
- Which three changes would improve the framework most?

## How to record it

Use one issue per reviewer, titled "Review: [level or scope], [month year]", containing their answers. Fix what is clearly wrong, and for each point you do not act on, reply with the reason. Then add a short entry to [docs/references.md](references.md):

> Reviewed by [name or "an anonymous safeguarding specialist"], [role], on [date], scope: [levels]. Changes made: [issue link].

Rules for the record:

- **Name a reviewer only with their written permission.** An anonymous entry is fine.
- **State the scope.** "Reviewed Level 4" is not "reviewed the framework".
- **Never write "approved", "endorsed", "certified", or "compliant".** A review found things, and you fixed some of them. That is all it shows.
- **Keep disagreement visible.** If two reviewers disagree and you pick one, say so in the issue.
- **Re-review after big changes.** A new level or a change to the floor starts the clock again.

## Try it on a real organization too

A review by specialists tells you whether the guidance is right. A pilot tells you whether it is *usable*. Ask one or two small non-profits to complete an assessment, and watch where they hesitate. Offer to sit with them while they answer, without explaining, and write down every question they ask and every control they skip. Do not publish their answers. See [SECURITY.md](../SECURITY.md) on why assessment files are sensitive.

## What to say until this is done

> The framework was developed by [the authors] and has not yet had outside expert review. Treat it as a structured set of questions, not as expert-verified guidance.
