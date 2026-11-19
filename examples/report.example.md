# safeAI assessment: Example Community Services (fictional)

Assessor: Example assessor · Date: 2026-01-15 · Mode: both · Framework version: 0.1.0

> This report is generated from self-reported answers. It is a planning aid, not an audit, certification, or legal advice. Scores are indicative and depend entirely on the honesty and accuracy of the answers.

## Summary

**Overall: 60.2 / 100 (Developing)**

Coverage: 46 of 67 applicable controls answered (68.7%); 1 marked not applicable.
Unanswered controls are left out of the scores. The real position may be worse than shown. Use `--strict` to count them as `none`.

## What you can honestly say

*The AI is a guest, not an admin.*

| | Statement | Status from your answers |
|---|---|---|
| **SEE** | It sees only what your people are already allowed to see, minus what you wall off. | Partly supported (64.4) |
| **DO** | It does only what you grant, and it stops for a named person where it matters. | Partly supported (47.5) |
| **SAY** | It says nothing that contradicts what you stand for, and never poses as a person. | Partly supported (78.9) |
| **ANSWER** | You answer for it with a full record of every decision, and you can stop it. | Partly supported (61.9) |

Only describe a control as *enforced* if you answered `structural` and can show the evidence. Describe `procedural` as *requiring approval* and `guided` as *recommended*.

## The seven levels

| Level | Score | Structural | Procedural | Guided | None | Not assessed |
|---|---:|---:|---:|---:|---:|---:|
| L1 Data protection (SEE) | 64.9 | 2 | 2 | 2 | 2 | 0 |
| L2 Vendor and model trust (SEE) | 63.3 | 0 | 3 | 0 | 2 | 3 |
| L3 Delegation and authority (DO) | 44.4 | 1 | 3 | 0 | 3 | 1 |
| L4 Protection of the vulnerable (DO) | 50.0 | 0 | 3 | 2 | 3 | 3 |
| L5 Mission and values fidelity (SAY) | 66.7 | 0 | 2 | 2 | 1 | 4 |
| L6 The human boundary (SAY) | 90.0 | 2 | 2 | 0 | 0 | 4 |
| L7 Accountability and governance (ANSWER) | 61.9 | 2 | 2 | 1 | 4 | 6 |

## Action plan

### Critical gaps first

- **L3.03 Draft versus commit**: currently none, next step guided (target: structural)
- **L3.04 Irreversible actions are never autonomous**: currently none, next step guided (target: structural)
- **L3.07 Prompt-injection containment**: currently none, next step guided (target: structural)
- **L4.03 Images and identifying details of minors stay off AI paths**: currently none, next step guided (target: structural)
- **L4.04 No AI-initiated contact with minors without required adults**: currently none, next step guided (target: structural)
- **L1.04 Personal data is masked before it reaches the model**: currently guided, next step procedural (target: structural)
- **L4.02 Protected records blocked or masked by default**: currently guided, next step procedural (target: structural)

### Quick wins (low effort, weeks)

**L2.06 Your own commitment on constituent data** · high · currently none, next step guided (target: procedural)
- [ ] Decide and write down what you will never do with constituent data, whatever a vendor permits.
- [ ] Publish it in plain language where constituents and partners can find it.
- [ ] Hold yourself to it through your governance process (see L7).

**L4.02 Protected records blocked or masked by default** · critical · currently guided, next step procedural (target: structural)
- [ ] Add the records from L4.01 to your block or mask list (see L1.03 and L1.04).
- [ ] Cover vulnerable adults with the same protections as minors.

**L4.06 Urgent need is never queued behind review** · high · not yet assessed. Answer it first (target: structural)
- [ ] Give urgent-need items a priority path that reaches a person immediately.
- [ ] Make it a rule that review of tone, mission, or policy never delays help.

**L5.04 Your values are authored by you** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Have your board or leadership adopt the values through your normal process.
- [ ] If you build software, set floors only for safeguarding and data protection. Never ship values or doctrine as a default.

**L6.03 No simulated care, friendship, or companionship** · high · not yet assessed. Answer it first (target: procedural)
- [ ] State the rule: the AI drafts, and a person cares.
- [ ] Require a human sender for care and support messages.
- [ ] Pay special attention to isolated, grieving, and dependent people, who are most at risk of mistaking simulation for relationship.

**L7.04 Responsibility map** · high · not yet assessed. Answer it first (target: procedural)
- [ ] For each AI deployment, write who is responsible for the model, the integration, the data, the configuration, and the decisions.
- [ ] Share it with leadership and, where relevant, with the people affected.

**L7.10 Impact assessment before higher-risk use** · high · currently none, next step guided (target: procedural)
- [ ] Use a one-page checklist: who is affected, what could go wrong, what safeguards exist, who signs.
- [ ] Include the voice of the people affected, or those who represent them.
- [ ] Attach it to the grant record (see L3.05).

**L7.12 Claims discipline** · high · currently none, next step guided (target: procedural)
- [ ] Before publishing a safety claim, find the control behind it and check its guarantee type.
- [ ] Say enforced only for structural controls. Say recommended or guided for the rest.
- [ ] Do not describe roadmap items in the present tense.

**L2.03 Model and sub-processor inventory** · medium · currently none, next step guided (target: procedural)
- [ ] Publish a one-page statement listing each model, vendor, sub-processor, and processing region.
- [ ] Update it when you change model or vendor.

**L2.05 Vendor safety rules and values are known** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Read the vendor's published usage policy and model documentation.
- [ ] Tell leadership and, where relevant, constituents that your own rules sit on top of the vendor's, so nobody discovers a second, invisible value layer on their own.

**L2.07 Environmental and labor due diligence** · medium · not yet assessed. Answer it first (target: guided)
- [ ] Ask each vendor for its published environmental and labor disclosures.
- [ ] Record what you found and how it informed your choice.

**L2.08 Re-assessment on vendor or model change** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Subscribe to vendor change notices.
- [ ] Make a model or terms change a trigger in your change-control process (see L7.14).

**L4.10 No appeals that exploit vulnerability** · high · currently guided, next step procedural (target: procedural)
- [ ] State in policy that AI-assisted appeals may not target vulnerability.
- [ ] Add a review step for AI-drafted appeals, including the segments they target.

**L5.06 Open questions are marked as opinion** · medium · not yet assessed. Answer it first (target: guided)
- [ ] List the questions where your organization deliberately holds no position.
- [ ] Tell the AI to present them as open and to avoid taking sides in your name.
- [ ] Do not block content for taking a side. Check only that it is marked as opinion.

**L5.09 Corrections can come from below** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Publish how to suggest a change to the AI rules.
- [ ] Review proposals on a schedule and record the outcome.

**L6.06 Positive scope: what the AI is for** · medium · not yet assessed. Answer it first (target: guided)
- [ ] For each boundary, write what the AI can still legitimately help with.
- [ ] Include these in the AI's instructions.

**L7.11 Staff AI literacy** · medium · not yet assessed. Answer it first (target: guided)
- [ ] Run a short session (one hour) on hallucination, bias, privacy, and the limits of the AI.
- [ ] Repeat for new staff, and refresh when tools change.

**L7.14 Change control and review rhythm** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Give every policy and rule set a version number and date.
- [ ] Review at least annually, and on any material change of model, vendor, or use.
- [ ] Changes to firm commitments trigger re-testing and sign-off.

### Build next (medium effort, a few months)

**L3.03 Draft versus commit** · critical · currently none, next step guided (target: structural)
- [ ] Split each write or send action into a staged step and a commit step.
- [ ] Make the commit step a human action in the tool itself, not a convention.
- [ ] Show approvers what will change, not only the AI's summary of it.

**L3.04 Irreversible actions are never autonomous** · critical · currently none, next step guided (target: structural)
- [ ] Define irreversible: anything that cannot be fully undone or that reaches many people.
- [ ] Enforce a human commit for those actions in code, regardless of role or grant.
- [ ] Hold mass updates above a set threshold for approval.

**L4.03 Images and identifying details of minors stay off AI paths** · critical · currently none, next step guided (target: structural)
- [ ] Exclude photo and file fields for minors from every AI integration.
- [ ] Mask age group, grade, and guardian links by default.
- [ ] Check which file and image tools your AI integrations expose, and disable the ones that reach these files.

**L4.04 No AI-initiated contact with minors without required adults** · critical · currently none, next step guided (target: structural)
- [ ] Add a recipient rule on every send path that checks for minors and required copies.
- [ ] Hold, and do not send, any message that fails the rule.

**L1.04 Personal data is masked before it reaches the model** · critical · currently guided, next step procedural (target: structural)
- [ ] Put a masking layer between your data and the AI so masking cannot be bypassed with a clever prompt.
- [ ] Define the list of masked fields and review it each quarter.
- [ ] Verify with test records that real values never appear in what is sent to the model.

**L1.05 Personal data inside free text is detected** · high · currently none, next step guided (target: structural)
- [ ] Test whether a phone number or disclosure typed into a notes field reaches the AI unmasked.
- [ ] Add pattern-based detection (and, where warranted, entity recognition) for free-text fields.
- [ ] Where detection is imperfect, block free-text fields on the most sensitive records instead.

**L1.08 Privacy obligations cover AI use** · high · currently none, next step guided (target: procedural)
- [ ] Check which privacy laws and funder or regulator rules apply to you (verify with qualified legal advice).
- [ ] Update your privacy notice to describe AI processing in plain language.
- [ ] Complete a data protection impact assessment where your jurisdiction requires or recommends one.

**L4.09 AI scores and classifications of people are visible** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Inventory every place an AI assigns a score, tag, risk level, or category to a person.
- [ ] Show it to staff with the factors behind it.
- [ ] Retire any that cannot be explained.

**L4.11 Protections are on by default and can only be raised** · high · not yet assessed. Answer it first (target: structural)
- [ ] Ship the protected-persons rules switched on.
- [ ] Make them non-waivable at the customer or chapter level. Allow tightening only.
- [ ] Do not shift the burden of control onto the families or administrators who might not find the setting.

**L5.03 Enforced commitments are separated from guidance** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Mark each commitment as enforced in code, enforced by a person, or guidance only.
- [ ] Compile only firm commitments that a machine can check into rules. Flexible ones become at most a review flag, and open ones are never turned into rules.
- [ ] Show the result to leadership and reviewers.

**L5.07 Behavioral regression tests** · high · currently none, next step guided (target: procedural)
- [ ] Write 20 to 50 test prompts that probe your red lines and the ways AI tends to drift from your values.
- [ ] Record expected and unacceptable answers. Have a person judge the results.
- [ ] Re-run on every model, prompt, or values-file change and keep the results.

**L6.05 Confidential disclosures are never solicited or recorded by AI** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Define what counts as confidential or privileged in your work.
- [ ] Add content rules on writes and sends that hold and route such content to a person.

**L7.06 Log records authority, not only activity** · high · currently none, next step guided (target: structural)
- [ ] Add grant, signer, policy version, override, and escalation-or-delegation fields to the log schema.
- [ ] Test that a reviewer can reconstruct why an action was allowed.

**L7.08 AI incident response** · high · currently none, next step guided (target: procedural)
- [ ] Add AI scenarios to your existing incident plan.
- [ ] Define who decides, who is notified (including regulators, funders, and affected people where required), and how lessons are recorded.
- [ ] Run a tabletop exercise once a year.

**L7.09 Recourse for affected people** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Tell affected people how to ask for a human review.
- [ ] Make sure the log (see L7.05, L7.06) lets staff reconstruct the decision.
- [ ] Record the outcome of each review.

**L3.01 Allow-list of AI actions, deny by default** · critical · currently procedural, next step structural (target: structural)
- [ ] List the action classes your AI integrations can perform.
- [ ] Grant each explicitly to specific roles. Treat anything unlisted as denied.
- [ ] Review grants at least twice a year.

**L3.06 Escalation is designed, not an error path** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Define the conditions that require a person: sensitive topics, uncertainty, conflict with a firm rule, high impact.
- [ ] When a firm rule conflicts with an instruction, hold and surface the conflict to the requester. Never silently comply or silently refuse.
- [ ] Record each handoff: the request, the proposed action, the rule, the risk.

**L5.05 Claims are sourced and estimates are marked** · high · currently guided, next step procedural (target: procedural)
- [ ] Require a source for factual claims and for statements about your own positions.
- [ ] Mark estimates and uncertainty explicitly in drafts.
- [ ] Hold, and do not block, content with unsourced claims, so a reviewer can decide.

**L6.01 No signing as a person without their approval** · critical · currently procedural, next step structural (target: structural)
- [ ] Check sender identity and signature block on every outbound message.
- [ ] Hold messages that carry a person's name or signature without that person's approval of the specific message.

**L6.07 Guarding against over-reliance** · medium · not yet assessed. Answer it first (target: procedural)
- [ ] Track how often reviewers edit or reject AI drafts. A rate near zero is a warning sign.
- [ ] Rotate reviewers and sample approved items for second review.

**L1.07 Pass-through handling and minimal retention** · high · currently procedural, next step structural (target: structural)
- [ ] Document what each AI integration stores, where, and for how long.
- [ ] Set retention limits and automatic deletion for prompts, outputs, and caches.
- [ ] Keep personal data out of logs, or mask it there as well.

**L2.02 Organization-managed accounts, not personal logins** · high · currently procedural, next step structural (target: structural)
- [ ] Provide approved AI tools on organization-managed accounts.
- [ ] Use single sign-on where available, so removing a person removes their access.
- [ ] Where you cannot technically block personal accounts, say plainly that this control is procedural or guided.

### Longer term (high effort)

**L3.07 Prompt-injection containment** · critical · currently none, next step guided (target: structural)
- [ ] Tag any action proposed while the AI was reading external content with a provenance flag.
- [ ] Apply stricter rules, or a mandatory human commit, to flagged actions.
- [ ] Test with documents that contain hidden instructions (see L7.13).

**L4.08 Fairness checks on AI rankings** · high · currently none, next step guided (target: procedural)
- [ ] Choose the groups relevant to your work and the data you can lawfully use to check them.
- [ ] Compare outcomes across groups on a sample before go-live, then periodically.
- [ ] Document what you checked and what you changed.

**L7.13 Red-team testing** · high · not yet assessed. Answer it first (target: procedural)
- [ ] Seed known violations (a message to a minor, a hidden instruction in an upload, an attempt to read a blocked record).
- [ ] Confirm each is caught. Keep the results as a regression suite.
- [ ] Re-run on every material change.

**L7.15 Policy inheritance across chapters or affiliates** · medium · not yet assessed. Answer it first (target: structural)
- [ ] Define which rules are set centrally and which are local.
- [ ] Let local units tighten central rules, never loosen them.
- [ ] Let local units propose changes to the center (see L5.09).

## All controls

| ID | Control | Severity | Answer | Strongest possible |
|---|---|---|---|---|
| L1.01 | Data inventory and classification | high | Procedural | procedural |
| L1.02 | AI inherits the user's own permissions | critical | Structural | structural |
| L1.03 | Restricted data is blocked from AI paths by default | critical | Structural | structural |
| L1.04 | Personal data is masked before it reaches the model | critical | Guided | structural |
| L1.05 | Personal data inside free text is detected | high | None | structural |
| L1.06 | Staff know what not to paste into AI tools | high | Guided | guided |
| L1.07 | Pass-through handling and minimal retention | high | Procedural | structural |
| L1.08 | Privacy obligations cover AI use | high | None | procedural |
| L2.01 | Vendor data terms reviewed | critical | Procedural | procedural |
| L2.02 | Organization-managed accounts, not personal logins | high | Procedural | structural |
| L2.03 | Model and sub-processor inventory | medium | None | procedural |
| L2.04 | Contracts and data processing terms | high | Procedural | procedural |
| L2.05 | Vendor safety rules and values are known | medium | Not assessed | procedural |
| L2.06 | Your own commitment on constituent data | high | None | procedural |
| L2.07 | Environmental and labor due diligence | medium | Not assessed | guided |
| L2.08 | Re-assessment on vendor or model change | medium | Not assessed | procedural |
| L3.01 | Allow-list of AI actions, deny by default | critical | Procedural | structural |
| L3.02 | Write and send capabilities are off until a decision is recorded | high | Procedural | procedural |
| L3.03 | Draft versus commit | critical | None | structural |
| L3.04 | Irreversible actions are never autonomous | critical | None | structural |
| L3.05 | Every grant has a named signer | high | Procedural | procedural |
| L3.06 | Escalation is designed, not an error path | medium | Not assessed | procedural |
| L3.07 | Prompt-injection containment | critical | None | structural |
| L3.08 | Volume and rate limits | high | Structural | structural |
| L3.09 | Policy travels with delegated work | medium | N/A | structural |
| L4.01 | Protected people and records are defined | critical | Procedural | procedural |
| L4.02 | Protected records blocked or masked by default | critical | Guided | structural |
| L4.03 | Images and identifying details of minors stay off AI paths | critical | None | structural |
| L4.04 | No AI-initiated contact with minors without required adults | critical | None | structural |
| L4.05 | Abuse, self-harm, and crisis content goes to a person | critical | Procedural | procedural |
| L4.06 | Urgent need is never queued behind review | high | Not assessed | structural |
| L4.07 | AI informs; people decide eligibility and priority | critical | Procedural | procedural |
| L4.08 | Fairness checks on AI rankings | high | None | procedural |
| L4.09 | AI scores and classifications of people are visible | high | Not assessed | procedural |
| L4.10 | No appeals that exploit vulnerability | high | Guided | procedural |
| L4.11 | Protections are on by default and can only be raised | high | Not assessed | structural |
| L5.01 | Mission and commitments are written down for AI | high | Procedural | procedural |
| L5.02 | Values file is given to the AI as context | medium | Guided | guided |
| L5.03 | Enforced commitments are separated from guidance | high | Not assessed | procedural |
| L5.04 | Your values are authored by you | high | Not assessed | procedural |
| L5.05 | Claims are sourced and estimates are marked | high | Guided | procedural |
| L5.06 | Open questions are marked as opinion | medium | Not assessed | guided |
| L5.07 | Behavioral regression tests | high | None | procedural |
| L5.08 | Public-facing AI content is reviewed before release | high | Procedural | procedural |
| L5.09 | Corrections can come from below | medium | Not assessed | procedural |
| L6.01 | No signing as a person without their approval | critical | Procedural | structural |
| L6.02 | AI is disclosed where it matters | high | Structural | structural |
| L6.03 | No simulated care, friendship, or companionship | high | Not assessed | procedural |
| L6.04 | Roles that need a human route to one | critical | Procedural | procedural |
| L6.05 | Confidential disclosures are never solicited or recorded by AI | high | Not assessed | procedural |
| L6.06 | Positive scope: what the AI is for | medium | Not assessed | guided |
| L6.07 | Guarding against over-reliance | medium | Not assessed | procedural |
| L6.08 | A human is always reachable | high | Structural | structural |
| L7.01 | Named owner for AI | critical | Procedural | procedural |
| L7.02 | Approved AI use policy | high | Guided | guided |
| L7.03 | Register of AI systems and use cases | high | Procedural | procedural |
| L7.04 | Responsibility map | high | Not assessed | procedural |
| L7.05 | Audit log of AI activity | critical | Structural | structural |
| L7.06 | Log records authority, not only activity | high | None | structural |
| L7.07 | Kill switch | critical | Structural | structural |
| L7.08 | AI incident response | high | None | procedural |
| L7.09 | Recourse for affected people | high | Not assessed | procedural |
| L7.10 | Impact assessment before higher-risk use | high | None | procedural |
| L7.11 | Staff AI literacy | medium | Not assessed | guided |
| L7.12 | Claims discipline | high | None | procedural |
| L7.13 | Red-team testing | high | Not assessed | procedural |
| L7.14 | Change control and review rhythm | medium | Not assessed | procedural |
| L7.15 | Policy inheritance across chapters or affiliates | medium | Not assessed | structural |
