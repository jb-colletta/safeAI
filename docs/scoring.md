# How scoring works

Scores are a planning aid. They are indicative, not an audit result, and they depend entirely on the honesty of the answers.

## Answers

For each control you choose the strongest statement that is **true today**:

`none` (0) · `guided` (1) · `procedural` (2) · `structural` (3) · `na`

Leave it blank if you have not assessed it yet.

## Control score

```
target = rank of the control's max_guarantee      (guided=1, procedural=2, structural=3)
level  = min(rank of your answer, target)
score  = level / target                           (0 to 1)
```

Examples: a control whose strongest possible guarantee is *structural* scores 0.33 at guided, 0.67 at procedural, and 1.0 at structural. A control that can only ever be *guided* scores 1.0 at guided.

An answer stronger than the control's ceiling is reported as an error by `safeai check`, and capped when scoring.

## Weights

Each control carries a weight from its severity: critical 3, high 2, medium 1.

## Level, verb, and overall scores

```
score = sum(weight × control score) / sum(weight)      over scored controls only
```

computed for each level, for each verb (SEE, DO, SAY, ANSWER), and overall (all scored controls together). Results are shown on a 0 to 100 scale, rounded to one decimal place (half up).

Controls marked `na` are left out. **Unanswered controls are also left out**, and reported as lower *coverage*. A score built on few answers can look better than reality, so:

- reports state coverage prominently,
- a score is labeled **provisional** when fewer than half the applicable controls are answered,
- `--strict` (the "strict scoring" checkbox) counts unanswered controls as `none`. Use it before you share a result.

## Bands

| Overall | Band |
|---|---|
| 90 and above | Leading |
| 75 to 89.9 | Strong |
| 50 to 74.9 | Developing |
| 25 to 49.9 | Basic |
| below 25 | Exposed |

Bands are labels for conversation, not standards.

## "What you can honestly say"

For each verb, the report compares your answers with one plain statement (for example, for DO: *"It does only what you grant, and it stops for a named person where it matters."*):

| Status | Rule |
|---|---|
| Supported by your answers | verb score at least 80, and no *critical* control scored below 0.5 |
| Partly supported | verb score at least 40 |
| Not yet supported | otherwise |
| Not assessed | no answered controls |

## Claims without evidence

A control answered `procedural` or `structural` with neither a note nor evidence is listed as an unevidenced claim. Confirm it before you rely on or repeat it.

## Action plan

Each control that is not at its ceiling (and not `na`) becomes a plan item. Unanswered controls appear too, marked "answer it first".

```
priority = weight × (1 − score) / effort cost            (low 1, medium 2, high 3)
```

Items are grouped by effort: **quick wins** (low), **build next** (medium), **longer term** (high), each sorted by priority. A separate **critical gaps first** list shows critical controls that are not at their ceiling, with those at `none` or unanswered first.

## Two implementations

The Python scorer (`src/safeai/scoring.py`) and the browser scorer (`web/scoring.js`) implement these rules separately. `tests/test_web_parity.py` checks that they agree on the example assessment. If you change a rule, change both and this page.
