# The framework as an ontology

The framework is also published as an OWL ontology in Turtle: [`web/safeai.ttl`](../web/safeai.ttl). It gives every level and control a stable web address (IRI), so other tools can refer to a control precisely instead of copying its text.

Uses this makes possible:

- Opening the framework in any OWL or RDF editor to browse it, check it for consistency, or review proposed changes.
- Linking your own records to controls: for example, a mapping from controls to the sources behind them, a sector pack of extra controls, or a mapping to another framework, each kept in a separate file that imports this one.
- Querying the framework with SPARQL (for example, "every critical, quick-win control in the DO levels").

## The YAML is still the source of truth

`web/safeai.ttl` is generated from `src/safeai/data/safeai-framework.yaml` by `scripts/build_ontology.py`. Do not edit the Turtle file by hand: change the YAML, then rebuild.

```bash
python scripts/build_ontology.py
```

CI rebuilds the file and fails if the committed copy is out of date, the same way it checks `web/index.html`.

## Addresses

> **Provisional before version 1.0.** These addresses may change before 1.0, most likely to a permanent redirect service such as w3id.org. Until then, do not rely on them in data you cannot easily update. If they change after others have started using them, the old file will stay published with links from each old term to its new one. From 1.0 on, addresses are permanent.

| Thing | IRI |
|---|---|
| The ontology | `https://jb-colletta.github.io/safeAI/safeai.ttl` |
| Namespace (prefix `sai:`) | `https://jb-colletta.github.io/safeAI/safeai.ttl#` |
| A level | `sai:L3` |
| A control | `sai:L3.04` (the control id, unchanged) |
| A verb | `sai:SEE`, `sai:DO`, `sai:SAY`, `sai:ANSWER` |
| A guarantee type | `sai:structural`, `sai:procedural`, `sai:guided`, `sai:none` |
| Audience, severity, effort | `sai:audience-product`, `sai:severity-critical`, `sai:effort-low` |

Control ids are permanent, and from version 1.0 control IRIs will be too. For now the namespace is a hash IRI on the project's published site, so it resolves to the Turtle file itself.

## Model

**Classes:** `sai:Verb`, `sai:Level`, `sai:Control`, `sai:FloorControl` (a subclass of `sai:Control`), `sai:GuaranteeType`, `sai:Audience`, `sai:Severity`, `sai:Effort`.

Levels, controls, and the enumerated values are named individuals of these classes. Human-dignity floor controls are typed `sai:FloorControl`, so a tool can find the floor without reading a flag.

**Properties:**

| YAML field | Property | Kind |
|---|---|---|
| level `verb` | `sai:verb` | object, functional |
| control `layer` | `sai:level` | object, functional |
| `max_guarantee` | `sai:maxGuarantee` | object, functional |
| `audience` | `sai:audience` | object (one or two values) |
| `severity` / `effort` | `sai:severity` / `sai:effort` | object, functional |
| `number`, `rank` | `sai:number`, `sai:rank` | integer |
| `quick_win` | `sai:quickWin` | boolean |
| `id` | `skos:notation` | annotation |
| `title`, level `name`, `label` | `rdfs:label` | annotation |
| `question`, `tagline`, `harm`, `summary`, `meaning`, `example`, `fails_by`, `evidence`, `floor_principle` | `sai:question`, `sai:tagline`, … | annotation |
| `steps` | `sai:step` | annotation, one value per step |

Text fields are annotation properties, so a reasoner ignores them and editors show them as notes. Each `sai:step` value starts with its position (`"1. "`), because annotation values have no order of their own.

The file also states that the individuals in each group are distinct (`owl:AllDifferent`). With the functional properties, this lets a reasoner flag a control that has been given two levels or two maximum guarantees.

## What is deliberately not in the ontology

- **Assessments.** Answers stay with the people who wrote them, in their own JSON or YAML files. The ontology describes the framework, not anyone's results.
- **Scoring rules.** Scoring lives in `scoring.py` and `scoring.js`, which tests keep in agreement. See [scoring.md](scoring.md).
- **Sources or values behind controls.** Anyone who wants to record them can do so in a separate ontology that imports this one and refers to controls by IRI. The core stays generic, in line with [floors, never doctrine](../CONTRIBUTING.md).
