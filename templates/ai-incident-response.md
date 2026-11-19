# AI incident response note (template)

> **How to use this template.** Fill in the brackets, remove steps you will not follow, and keep it to one or two pages that someone can use under stress. Where a law or contract sets a deadline or a duty to notify, have a qualified adviser confirm what applies to you and write it in. This template does not state any legal deadline. It relates to control L7.08.

**Organization:** [Organization name]
**Incident lead:** [Named role] **Backup:** [Named role]
**Contacts:** [Executive owner for AI], [Privacy lead], [Safeguarding lead], [AI vendor contact], [Adviser]
**Version:** [1.0] **Last tested:** [date]

## What counts as an AI incident

- Personal or sensitive data reached an AI tool or person it should not have, or may have leaked.
- An AI sent a message it should not have, or one that is harmful, false, or contradicts our commitments.
- An AI took a wrong action: changed or deleted records, or contacted the wrong people.
- Content about a child, abuse, self-harm, or immediate danger was handled by AI without a person.
- An AI score or recommendation about a person was wrong, hidden, or unfair.
- Someone tried to manipulate the AI, for example with instructions hidden in a document.

## First hour

1. **Tell the incident lead** at [how]. Anyone may report. Nobody is blamed for reporting.
2. **Stop it.** Use the switch that turns off AI access for one user, one tool, or everything. [L7.07] Decide who may use it without asking first: [roles].
3. **If a person may be in danger,** act first through our safeguarding process: [steps and contact]. Do not wait for the investigation.
4. **Write down** what you know now, who knows it, and the time. Keep the logs. Do not delete anything.

## Understand it

- What happened, when, and which AI tool and account?
- Which data and which people are involved? Are any of them protected people (children, vulnerable adults, people in crisis)?
- Who granted the permission the AI used, and under which policy version? [L7.06]
- Did a person override or approve any step?
- Is it still happening, or could it happen again?

## Tell people

- **Internally:** [executive owner, governing body, who else and when].
- **People affected:** [who tells them, in what words, through which named person]. Affected people are told plainly what happened and how to ask for a human review of anything decided about them. [L7.09]
- **The vendor:** [contact, using the terms in our contract]. [L2.04]
- **Regulators, funders, insurers, or others:** [list, only after an adviser confirms what applies and when].

Do not describe a protection as enforced in these messages unless it was. [L7.12]

## Fix and learn

1. Correct harm to people first: restore records, retract messages, support those affected.
2. Find the cause and which control should have prevented it. Was that control structural, procedural, or only guided?
3. If a guided control failed, decide whether to make it procedural or structural.
4. Re-run the assessment for the affected controls, and re-run behavior tests where a model or prompt was involved. [L5.07, L2.08]
5. Record the incident, decisions, and changes in [where]. Update the AI register and policy if needed. [L7.03, L7.14]
6. Review the incident with [group] within [period].

## Test this note

At least [once a year], walk through a made-up incident using this note. Record what was unclear and fix it.
