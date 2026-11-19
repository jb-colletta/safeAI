# The human-dignity floor

Most of safeAI lets an organization decide how much safety to build and in what order. A small part of it does not. Eleven controls form a **floor**: a minimum that any organization using or building AI for people should have in place before it describes its position as strong.

## The idea

Every person has worth that does not depend on what they produce, achieve, or cost. An AI system that decides, ranks, speaks to, or stands in for people can quietly act as if it does. The floor asks whether you have put safeguards in place so that it cannot, and so that a person always answers for what it does.

The floor is deliberately small and deliberately about people, not about any organization's mission. It sets what must hold for everyone. **What your organization stands for, beyond this, is yours to write** (Level 5), and you can only add to the floor, never go below it.

## The eleven floor controls

| Control | What it protects |
|---|---|
| L3.04 Irreversible actions are never autonomous | Serious or irreversible decisions stay with people. |
| L4.03 Images and identifying details of minors stay off AI paths | Children's images and identifying details are kept off AI paths. |
| L4.04 No AI-initiated contact with minors without required adults | The AI does not contact children without the required adults. |
| L4.07 AI informs; people decide eligibility and priority | People, not algorithms, decide who receives help. |
| L4.09 AI scores and classifications of people are visible | How the AI measures and ranks people is visible, not hidden. |
| L4.11 Protections are on by default and can only be raised (products) | Protecting the vulnerable is the provider's burden and cannot be weakened. |
| L4.12 A person's worth is never scored by usefulness | A person's worth is never scored by what they produce. |
| L6.02 AI is disclosed where it matters | The AI never passes as a person. |
| L6.03 No simulated care, friendship, or companionship | Simulated care is never presented as a real relationship. |
| L7.04 Responsibility map | Someone identifiable answers for the AI at every stage. |
| L7.09 Recourse for affected people | Anyone affected can appeal to a human. |

Floor controls carry `floor: true` and a one-sentence `floor_principle` in the framework file. L4.11 applies to products only, so it is left out when you assess as an organization.

## How the floor affects your result

- A floor control is **met** when you answer **procedural or structural**. Guided is not enough: telling people to be careful does not guarantee anyone's dignity.
- If any floor control is answered below that, the floor is **not met**. If none is below it but some are unanswered, the floor is **not yet confirmed**. In `--strict` mode unanswered controls count as `none`, so they make the floor not met.
- While the floor is not met or not confirmed, the **overall rating is held at Developing**, however well the rest scores. Your numeric score is not changed, and the report shows both the held rating and the rating you would otherwise have.
- A floor control marked **not applicable** counts as met, but the report lists it so you are asked to confirm that it really does not apply.
- The action plan lists floor gaps **before** everything else.

## What the floor is not

- It does **not** show that your AI upholds anyone's dignity. It shows that you report having safeguards in place. Answers are self-reported and unaudited.
- It is **not** a statement of anyone's beliefs or a certification. Describe your result as "we have assessed ourselves against a human-dignity floor and here is where we stand", never as "dignity-compliant" or "ethical".
- It does **not** replace local law, funder requirements, or professional safeguarding standards. It sets a minimum underneath them.

## Changing the floor

The floor should change rarely and for good reason. To propose adding, removing, or rewording a floor control, open an issue that explains the harm it addresses and who is affected. Floor controls must allow at least a procedural guarantee, and the framework validator enforces that.
