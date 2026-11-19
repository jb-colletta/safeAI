# The safeAI framework

## Why seven levels

A security reviewer asks about data. A safeguarding lead asks about children. A program director asks whether the AI will misstate your mission. A board asks who is responsible. These are different people asking different questions, and "we encrypt everything" answers only the first.

The seven levels group into four verbs:

| Verb | Levels | Concern |
|---|---|---|
| **SEE** | 1 Data protection, 2 Vendor and model trust | What the AI can learn, and who else learns it |
| **DO** | 3 Delegation and authority, 4 Protection of the vulnerable | What the AI can change or send, and who it could hurt |
| **SAY** | 5 Mission and values fidelity, 6 The human boundary | What is said in your name, and whether a person is behind it |
| **ANSWER** | 7 Accountability and governance | Who is responsible, and whether you can see and stop it |

Two concerns people often raise are deliberately folded into these levels rather than given their own. **Accuracy** (made-up facts) lives in Level 5, as sourcing and marking estimates. **Fairness** in AI ranking (care queues, aid, outreach) lives in Level 4, because the people harmed are, almost by definition, the least able to notice.

## Three kinds of guarantee

Every control has a strongest realistic guarantee (`max_guarantee`). Your answer says how it is guaranteed *today*:

- **Structural**: enforced in code or configuration. It cannot happen, whatever the AI does or is told. Example: a phone number is masked by the server before the AI receives it. A prompt cannot recover data the server never sent.
- **Procedural**: it cannot happen without a named person's approval or a recorded process. Example: write access stays off until an administrator signs a recorded decision.
- **Guided**: people or the AI are told what to do and usually comply. Nothing ensures it. Example: staff are told not to paste personal data into a chatbot.
- **None**: no control exists yet.

Some controls can only ever be guided (for example, teaching staff what the AI cannot do). For those, an honest "guided" earns full credit. For a control that *can* be structural, "guided" earns partial credit, which is the point: it shows the distance still to travel.

## Design principles

These shape which controls are in the framework.

1. **The AI is a guest, not an admin.** It sees only what the people using it can already see, minus what you wall off. It does only what you grant.
2. **Enforce at the action, not the prompt.** Filters on what goes *in* can be fooled, especially by instructions hidden in documents the AI reads. The reliable place for a control is the moment before an action takes effect.
3. **Allow-list first.** Say what the AI may do. Everything else is denied. A list of prohibitions always has a gap.
4. **Separate drafting from committing.** The AI may draft or stage. A person commits or sends, especially for anything irreversible or that reaches many people.
5. **AI informs; people decide.** Eligibility, priority, and access to help are decided by a named person, whose decision is recorded, and affected people can ask for a human review.
6. **The AI drafts; a person cares.** AI must not simulate care or companionship, pose as a person, or stand in for roles that need a human.
7. **Floors, never doctrine.** A toolkit or a software provider can set minimum protections for safeguarding and data. It must never supply your values. Those are authored by your organization, through your own governance, and open to correction from the people they govern.
8. **Pause on policy, never on help.** Review queues for tone or mission must never delay a response to urgent human need.
9. **Be honest about what is enforced.** Never describe a guided control as structural.

## Reading a control

Each control in `safeai-framework.yaml` has:

| Field | Meaning |
|---|---|
| `id` | Stable identifier such as `L4.02`. Never reused. |
| `question` | A plain-language self-assessment question |
| `audience` | `organization` (uses AI tools), `product` (builds AI features), or both |
| `max_guarantee` | The strongest realistic guarantee |
| `severity` | `critical`, `high`, or `medium`: how bad a gap is |
| `effort` | `low`, `medium`, or `high`: rough cost to close it |
| `quick_win` | A typical organization can close it in weeks |
| `steps` | Concrete actions that close the gap |
| `evidence` | What a reviewer could look at to confirm your answer |

## Organizations and products

An **organization** answers for how its staff and volunteers use AI tools and for the AI features in the systems it runs. A **product** team answers for what it ships: the defaults, the limits, the logs. If you are a software provider serving non-profits, assess your product in `product` mode, and encourage your customers to assess themselves in `organization` mode. Where the two meet (for example, protections on by default, or recourse for affected people), the controls appear for both.
