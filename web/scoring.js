/*
 * safeAI scoring, used by the browser tool (web/index.html) and tested against the
 * Python implementation (src/safeai/scoring.py). If you change a rule here, change it
 * there and in docs/scoring.md. `tests/test_web_parity.py` will fail if they drift.
 */
(function (root) {
  'use strict';

  var RANK = { none: 0, guided: 1, procedural: 2, structural: 3 };
  var RANK_NAME = ['none', 'guided', 'procedural', 'structural'];
  var WEIGHT = { critical: 3, high: 2, medium: 1 };
  var COST = { low: 1, medium: 2, high: 3 };
  var BANDS = [[90, 'Leading'], [75, 'Strong'], [50, 'Developing'], [25, 'Basic'], [0, 'Exposed']];
  var ANSWERS = ['none', 'guided', 'procedural', 'structural', 'na'];
  var VERB_CLAUSES = {
    SEE: 'It sees only what your people are already allowed to see, minus what you wall off.',
    DO: 'It does only what you grant, and it stops for a named person where it matters.',
    SAY: 'It says nothing that contradicts what you stand for, and never poses as a person.',
    ANSWER: 'You answer for it with a full record of every decision, and you can stop it.'
  };
  var STATUS_TEXT = {
    supported: 'Supported by your answers',
    partly: 'Partly supported',
    not_yet: 'Not yet supported',
    unassessed: 'Not assessed'
  };
  var ANSWER_LABEL = {
    structural: 'Structural', procedural: 'Procedural', guided: 'Guided',
    none: 'None', na: 'N/A', '': 'Not assessed'
  };
  var DISCLAIMER =
    'This report is generated from self-reported answers. It is a planning aid, not an audit, ' +
    'certification, or legal advice. Scores are indicative and depend entirely on the honesty ' +
    'and accuracy of the answers.';

  function pct(x) { return Math.floor(x * 1000 + 0.5) / 10; }
  function r4(x) { return Math.floor(x * 10000 + 0.5) / 10000; }

  function bandFor(score) {
    if (score === null) return null;
    for (var i = 0; i < BANDS.length; i++) if (score >= BANDS[i][0]) return BANDS[i][1];
    return BANDS[BANDS.length - 1][1];
  }

  function applies(control, mode) {
    return mode === 'both' || control.audience.indexOf(mode) !== -1;
  }

  function emptyEntry() { return { answer: '', note: '', evidence: '' }; }

  function weighted(rows) {
    var total = 0, sum = 0;
    rows.forEach(function (r) { total += r.weight; sum += r.weight * r.score; });
    return total ? sum / total : null;
  }

  function counts(rows) {
    var c = { structural: 0, procedural: 0, guided: 0, none: 0, unanswered: 0, na: 0 };
    rows.forEach(function (r) {
      if (r.status === 'scored') c[RANK_NAME[r.level]] += 1;
      else if (r.status === 'na') c.na += 1;
      else c.unanswered += 1;
    });
    return c;
  }

  function compute(framework, assessment, strict) {
    var scope = assessment.scope || {};
    var mode = scope.mode || 'both';
    var answers = assessment.answers || {};
    var rows = [];

    framework.controls.forEach(function (control) {
      if (!applies(control, mode)) return;
      var entry = answers[control.id] || emptyEntry();
      var ans = entry.answer || '';
      var target = RANK[control.max_guarantee];
      var row = {
        id: control.id, layer: control.layer, title: control.title,
        severity: control.severity, effort: control.effort, quick_win: !!control.quick_win,
        max_guarantee: control.max_guarantee, target: target, answer: ans,
        note: entry.note || '', evidence: entry.evidence || '',
        weight: WEIGHT[control.severity], level: null, score: null,
        status: 'unanswered', capped: false, unevidenced: false
      };
      if (ans === 'na') {
        row.status = 'na';
      } else {
        if (ans === '' && strict) { ans = 'none'; row.answer = 'none'; }
        if (Object.prototype.hasOwnProperty.call(RANK, ans)) {
          var level = RANK[ans];
          if (level > target) { level = target; row.capped = true; }
          row.level = level;
          row.score = level / target;
          row.status = 'scored';
          if (level >= 2 && !row.note.trim() && !row.evidence.trim()) row.unevidenced = true;
        }
      }
      rows.push(row);
    });

    var layers = framework.layers.map(function (layer) {
      var lrows = rows.filter(function (r) { return r.layer === layer.id; });
      var scored = lrows.filter(function (r) { return r.status === 'scored'; });
      var s = weighted(scored);
      return {
        id: layer.id, number: layer.number, name: layer.name, verb: layer.verb,
        tagline: layer.tagline, score: s === null ? null : pct(s),
        total: lrows.filter(function (r) { return r.status !== 'na'; }).length,
        answered: scored.length, counts: counts(lrows)
      };
    });

    var verbOf = {};
    framework.layers.forEach(function (l) { verbOf[l.id] = l.verb; });
    var verbs = Object.keys(framework.verbs).map(function (verb) {
      var vrows = rows.filter(function (r) { return verbOf[r.layer] === verb; });
      var scored = vrows.filter(function (r) { return r.status === 'scored'; });
      var s = weighted(scored);
      var status;
      if (s === null) status = 'unassessed';
      else {
        var weakCritical = scored.some(function (r) { return r.severity === 'critical' && r.score < 0.5; });
        if (s >= 0.8 && !weakCritical) status = 'supported';
        else if (s >= 0.4) status = 'partly';
        else status = 'not_yet';
      }
      return {
        verb: verb, label: framework.verbs[verb].label,
        score: s === null ? null : pct(s), status: status, clause: VERB_CLAUSES[verb]
      };
    });

    var scoredAll = rows.filter(function (r) { return r.status === 'scored'; });
    var os = weighted(scoredAll);
    var overall = { score: os === null ? null : pct(os) };
    overall.band = bandFor(overall.score);

    var applicable = rows.filter(function (r) { return r.status !== 'na'; });
    var coverage = {
      applicable: applicable.length,
      answered: applicable.filter(function (r) { return r.status === 'scored'; }).length,
      not_applicable: rows.filter(function (r) { return r.status === 'na'; }).length,
      total_in_mode: rows.length
    };
    coverage.percent = coverage.applicable ? pct(coverage.answered / coverage.applicable) : null;

    return {
      framework_version: framework.version, scope: scope, strict: !!strict,
      coverage: coverage, overall: overall, layers: layers, verbs: verbs, controls: rows,
      unevidenced: rows.filter(function (r) { return r.unevidenced; }).map(function (r) { return r.id; }),
      capped: rows.filter(function (r) { return r.capped; }).map(function (r) { return r.id; })
    };
  }

  function makePlan(result) {
    var items = [];
    result.controls.forEach(function (r) {
      if (r.status === 'na') return;
      if (r.status === 'scored' && r.score >= 1) return;
      var unanswered = r.status === 'unanswered';
      var score = unanswered ? 0 : r.score;
      var priority = r.weight * (1 - score) / COST[r.effort];
      items.push({
        id: r.id, title: r.title, severity: r.severity, effort: r.effort, quick_win: r.quick_win,
        current: unanswered ? 'unanswered' : RANK_NAME[r.level],
        target: RANK_NAME[r.target],
        next: unanswered ? null : RANK_NAME[Math.min(r.level + 1, r.target)],
        priority: r4(priority), assess_first: unanswered
      });
    });
    items.sort(function (a, b) {
      if (b.priority !== a.priority) return b.priority - a.priority;
      return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
    });
    var critical = items.filter(function (i) { return i.severity === 'critical'; });
    critical.sort(function (a, b) {
      var fa = (a.current === 'none' || a.current === 'unanswered') ? 1 : 0;
      var fb = (b.current === 'none' || b.current === 'unanswered') ? 1 : 0;
      if (fa !== fb) return fb - fa;
      return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
    });
    return {
      critical: critical,
      horizons: {
        quick: items.filter(function (i) { return i.effort === 'low'; }),
        next: items.filter(function (i) { return i.effort === 'medium'; }),
        later: items.filter(function (i) { return i.effort === 'high'; })
      },
      count: items.length
    };
  }

  /* -------- assessment files: JSON, or the YAML template written by `safeai init` ------- */

  function parseScalar(raw) {
    var s = raw.trim();
    if (s === '') return '';
    if (s.charAt(0) === '"') {
      var i = 1;
      while (i < s.length) {
        if (s.charAt(i) === '\\') { i += 2; continue; }
        if (s.charAt(i) === '"') break;
        i++;
      }
      return JSON.parse(s.slice(0, i + 1));
    }
    var hash = s.indexOf(' #');
    if (hash !== -1) s = s.slice(0, hash);
    return s.trim();
  }

  /* A deliberately tiny reader for the assessment layout only. It is not a general YAML parser. */
  function parseSimpleYaml(text) {
    var out = { scope: {}, answers: {} };
    var section = null, current = null;
    text.split(/\r?\n/).forEach(function (line) {
      if (/^\s*#/.test(line) || !line.trim()) return;
      var m;
      if ((m = /^(scope|answers):\s*$/.exec(line))) { section = m[1]; current = null; return; }
      if (/^\S/.test(line)) { section = null; return; }
      if (section === 'scope' && (m = /^\s{2}(\w+):\s*(.*)$/.exec(line))) {
        out.scope[m[1]] = parseScalar(m[2]);
      } else if (section === 'answers') {
        if ((m = /^\s{2}(L\d+\.\d+):\s*(.*)$/.exec(line))) {
          current = m[1];
          var rest = m[2].trim();
          out.answers[current] = { answer: '', note: '', evidence: '' };
          if (rest && rest.charAt(0) !== '#') out.answers[current].answer = parseScalar(rest).toLowerCase();
        } else if (current && (m = /^\s{4}(answer|note|evidence):\s*(.*)$/.exec(line))) {
          var v = parseScalar(m[2]);
          out.answers[current][m[1]] = m[1] === 'answer' ? String(v).toLowerCase() : v;
        }
      }
    });
    return out;
  }

  function parseAssessmentFile(text) {
    var raw;
    try { raw = JSON.parse(text); } catch (e) { raw = parseSimpleYaml(text); }
    return normalize(raw);
  }

  function normalize(raw) {
    var scope = Object.assign({ mode: 'both' }, raw.scope || {});
    var answers = {};
    Object.keys(raw.answers || {}).forEach(function (id) {
      var v = raw.answers[id];
      if (v && typeof v === 'object') {
        answers[id] = {
          answer: v.answer ? String(v.answer).trim().toLowerCase() : '',
          note: v.note ? String(v.note) : '', evidence: v.evidence ? String(v.evidence) : ''
        };
      } else {
        answers[id] = { answer: v ? String(v).trim().toLowerCase() : '', note: '', evidence: '' };
      }
    });
    return { scope: scope, answers: answers };
  }

  function exportAssessment(framework, assessment) {
    var answers = {};
    framework.controls.forEach(function (c) {
      var e = assessment.answers[c.id];
      if (e && (e.answer || e.note || e.evidence)) answers[c.id] = e;
    });
    return JSON.stringify({
      safeai_assessment: 1, framework_version: framework.version,
      scope: assessment.scope, answers: answers
    }, null, 2) + '\n';
  }

  /* -------- Markdown report (same structure as the CLI's) -------- */

  function fmt(x) { return x === null ? 'n/a' : x.toFixed(1); }

  function move(i) {
    if (i.assess_first) return 'not yet assessed. Answer it first (target: ' + i.target + ')';
    if (i.current === i.next) return 'currently ' + i.current;
    return 'currently ' + i.current + ', next step ' + i.next + ' (target: ' + i.target + ')';
  }

  function toMarkdown(result, plan, framework) {
    var byId = {};
    framework.controls.forEach(function (c) { byId[c.id] = c; });
    var L = [];
    var s = result.scope, o = result.overall, cov = result.coverage;
    L.push('# safeAI assessment: ' + (s.name || 'Untitled assessment'), '');
    var meta = [];
    if (s.assessor) meta.push('Assessor: ' + s.assessor);
    if (s.date) meta.push('Date: ' + s.date);
    meta.push('Mode: ' + (s.mode || 'both'));
    meta.push('Framework version: ' + result.framework_version);
    L.push(meta.join(' · '), '', '> ' + DISCLAIMER, '', '## Summary', '');
    L.push(o.score === null ? 'No controls have been answered yet, so there is no score.'
      : '**Overall: ' + fmt(o.score) + ' / 100 (' + o.band + ')**', '');
    if (o.score !== null && !result.strict && cov.percent !== null && cov.percent < 50) {
      L.push('**Provisional:** fewer than half of the applicable controls have been answered.', '');
    }
    L.push('Coverage: ' + cov.answered + ' of ' + cov.applicable + ' applicable controls answered' +
      (cov.percent !== null ? ' (' + fmt(cov.percent) + '%)' : '') +
      (cov.not_applicable ? '; ' + cov.not_applicable + ' marked not applicable' : '') + '.');
    if (cov.answered < cov.applicable && !result.strict) {
      L.push('Unanswered controls are left out of the scores. The real position may be worse than shown.');
    }
    L.push('', '## What you can honestly say', '', '*The AI is a guest, not an admin.*', '');
    L.push('| | Statement | Status from your answers |', '|---|---|---|');
    result.verbs.forEach(function (v) {
      L.push('| **' + v.verb + '** | ' + v.clause + ' | ' + STATUS_TEXT[v.status] + ' (' + fmt(v.score) + ') |');
    });
    L.push('', 'Only describe a control as *enforced* if you answered `structural` and can show the evidence. ' +
      'Describe `procedural` as *requiring approval* and `guided` as *recommended*.', '');
    L.push('## The seven levels', '');
    L.push('| Level | Score | Structural | Procedural | Guided | None | Not assessed |', '|---|---:|---:|---:|---:|---:|---:|');
    result.layers.forEach(function (l) {
      var c = l.counts;
      L.push('| L' + l.number + ' ' + l.name + ' (' + l.verb + ') | ' + fmt(l.score) + ' | ' + c.structural + ' | ' +
        c.procedural + ' | ' + c.guided + ' | ' + c.none + ' | ' + c.unanswered + ' |');
    });
    L.push('');
    if (result.unevidenced.length) {
      L.push('## Claims without evidence', '',
        'These controls were marked procedural or structural with no note or evidence. Confirm each before you rely on or repeat the claim.', '');
      result.unevidenced.forEach(function (id) { L.push('- ' + id + ' ' + byId[id].title); });
      L.push('');
    }
    L.push('## Action plan', '');
    if (!plan.count) {
      L.push('No gaps found among the controls you answered. Keep your evidence current.', '');
    } else {
      var crit = plan.critical.filter(function (i) { return ['none', 'unanswered', 'guided'].indexOf(i.current) !== -1; });
      if (crit.length) {
        L.push('### Critical gaps first', '');
        crit.forEach(function (i) { L.push('- **' + i.id + ' ' + i.title + '**: ' + move(i)); });
        L.push('');
      }
      var names = { quick: 'Quick wins (low effort, weeks)', next: 'Build next (medium effort, a few months)', later: 'Longer term (high effort)' };
      ['quick', 'next', 'later'].forEach(function (k) {
        var items = plan.horizons[k];
        if (!items.length) return;
        L.push('### ' + names[k], '');
        items.forEach(function (i) {
          L.push('**' + i.id + ' ' + i.title + '** · ' + i.severity + ' · ' + move(i));
          byId[i.id].steps.forEach(function (st) { L.push('- [ ] ' + st); });
          L.push('');
        });
      });
    }
    L.push('## All controls', '', '| ID | Control | Severity | Answer | Strongest possible |', '|---|---|---|---|---|');
    result.controls.forEach(function (r) {
      L.push('| ' + r.id + ' | ' + r.title + ' | ' + r.severity + ' | ' + ANSWER_LABEL[r.answer] + ' | ' + r.max_guarantee + ' |');
    });
    L.push('');
    return L.join('\n');
  }

  var api = {
    RANK: RANK, RANK_NAME: RANK_NAME, ANSWERS: ANSWERS, STATUS_TEXT: STATUS_TEXT,
    ANSWER_LABEL: ANSWER_LABEL, DISCLAIMER: DISCLAIMER, VERB_CLAUSES: VERB_CLAUSES,
    applies: applies, compute: compute, makePlan: makePlan, normalize: normalize,
    parseAssessmentFile: parseAssessmentFile, parseSimpleYaml: parseSimpleYaml,
    exportAssessment: exportAssessment, toMarkdown: toMarkdown, bandFor: bandFor, move: move, fmt: fmt
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SafeAI = api;
})(typeof self !== 'undefined' ? self : this);
