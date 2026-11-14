'use strict';

const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const outDir = process.argv[2] || path.resolve(__dirname, '../output');
const records = fs.readFileSync(path.join(outDir, 'records.jsonl'), 'utf8')
  .trim().split(/\r?\n/).map(JSON.parse);
const summary = JSON.parse(fs.readFileSync(path.join(outDir, 'summary.json'), 'utf8'));

function parseLog(file) {
  const text = fs.readFileSync(path.join(outDir, file), 'utf8');
  const status = (text.match(/^s (SATISFIABLE|UNSATISFIABLE)$/m) || [])[1];
  const conflicts = Number((text.match(/^c conflicts:\s*(\d+)/m) || [])[1]);
  const seconds = Number((text.match(/^c process-time:.* ([\d.]+) seconds/m) || [])[1]);
  assert.ok(status, file + ': missing final SAT status');
  assert.ok(Number.isFinite(conflicts), file + ': missing conflict count');
  assert.ok(Number.isFinite(seconds), file + ': missing process time');
  return {
    result: status === 'SATISFIABLE' ? 'SAT' : 'UNSAT',
    conflicts,
    seconds,
  };
}

function canonicalDeficiencyClass(rows, width) {
  const a = rows.slice().sort((x, y) => x - y);
  const b = a.map(y => width - 1 - y).sort((x, y) => x - y);
  const sa = a.join(',');
  const sb = b.join(',');
  return sa <= sb ? sa : sb;
}

function allCanonicalClasses(width) {
  const classes = new Set();
  for (let mask = 1; mask < (1 << width); mask++) {
    const rows = [];
    for (let y = 0; y < width; y++) if (mask & (1 << y)) rows.push(y);
    classes.add(canonicalDeficiencyClass(rows, width));
  }
  return [...classes].sort();
}

// 1. Reconcile every raw Kissat log with its JSONL record.
assert.equal(records.length, 52, 'record count');
const files = new Set();
for (const record of records) {
  assert.ok(!files.has(record.file), 'duplicate record file: ' + record.file);
  files.add(record.file);
  const log = parseLog(record.file);
  assert.equal(record.result, log.result, record.file + ': result');
  assert.equal(record.conflicts, log.conflicts, record.file + ': conflicts');
  assert.ok(Math.abs(record.seconds - log.seconds) < 0.011, record.file + ': seconds');
}

// 2. Check the exact deficiency-class partition.
const canonical = allCanonicalClasses(5);
assert.equal(canonical.length, 19, 'row-reflection class count');
const m21 = records.filter(r => r.m === 21);
assert.equal(m21.length, 51, 'm=21 record count');
assert.ok(m21.every(r => r.result === 'UNSAT'), 'all m=21 records must be UNSAT');
const direct = m21.filter(r => r.encoding === 'class');
assert.equal(direct.length, 17, 'direct class count');
const directClasses = direct.map(r =>
  canonicalDeficiencyClass(r.class.split(',').map(Number), 5)
).sort();
const expectedDirect = canonical.filter(c => c !== '0' && c !== '1');
assert.deepEqual(directClasses, expectedDirect, '17 direct classes must be exactly the classes other than {0},{1}');

// 3. Check the complete k x minpos decomposition for {0} and {1}.
const split = m21.filter(r =>
  r.encoding === 'class+krow' || r.encoding === 'class+krow+minpos'
);
assert.equal(split.length, 32, 'split instance count');
for (const y of ['0', '1']) {
  const group = split.filter(r => r.class === y);
  assert.equal(group.length, 16, 'split count for class {' + y + '}');
  for (let k = 0; k <= 4; k++) {
    const found = group.filter(r => r.krow === y + ':' + k && r.minpos == null);
    assert.equal(found.length, 1, 'exact-k split ' + y + ':' + k);
  }
  for (let p = 0; p <= 10; p++) {
    const found = group.filter(r => r.krow === y + ':5' && r.minpos === p);
    assert.equal(found.length, 1, 'minpos split ' + y + ':5:' + p);
    assert.equal(found[0].result, 'UNSAT', 'minpos result ' + y + ':' + p);
  }
}

// 4. Check the two independent H-reflection re-encodings and the SAT positive control.
const lex = m21.filter(r => r.encoding === 'class+lexH cross-check');
assert.equal(lex.length, 2, 'lex cross-check count');
assert.deepEqual(lex.map(r => r.class).sort(), ['0,1', '2']);
assert.ok(lex.every(r => r.result === 'UNSAT'));
const controls = records.filter(r => r.m === 18);
assert.equal(controls.length, 1, 'positive control count');
assert.equal(controls[0].result, 'SAT');

// 5. Check totals and the sharper minpos range.
const m21Conflicts = m21.reduce((sum, r) => sum + r.conflicts, 0);
assert.equal(m21Conflicts, 28617104);
assert.equal(summary.direct_classes_unsat, 17);
assert.equal(summary.class0_k_minpos_split_unsat, 16);
assert.equal(summary.class1_k_minpos_split_unsat, 16);
assert.equal(summary.indet, 0);
assert.equal(summary.total_conflicts_21, m21Conflicts);

// If x_1 < ... < x_k are k distinct columns in {0,...,m-1}, then
// p=min(x_1,m-1-x_k) <= floor((m-k)/2).  For (m,k)=(21,5), p<=8;
// p=9,10 are empty subinstances, retained in the original sweep.
const m = 21, k = 5;
const maxMinpos = Math.floor((m - k) / 2);
assert.equal(maxMinpos, 8);
let subsets = 0;
function enumerate(xs, start) {
  if (xs.length === k) {
    subsets++;
    const p = Math.min(xs[0], m - 1 - xs[k - 1]);
    assert.ok(p <= maxMinpos, 'minpos bound violated');
    return;
  }
  for (let x = start; x < m; x++) {
    xs.push(x);
    enumerate(xs, x + 1);
    xs.pop();
  }
}
enumerate([], 0);
assert.equal(subsets, 20349);

console.log(JSON.stringify({
  records: records.length,
  rawLogsMatched: records.length,
  m21Unsat: m21.length,
  directClasses: direct.length,
  splitInstances: split.length,
  lexCrossChecks: lex.length,
  positiveControls: controls.length,
  m21Conflicts,
  canonicalDeficiencyClasses: canonical.length,
  fiveStoneRowsEnumerated: subsets,
  minposUpperBound: maxMinpos,
  vacuousMinposCasesPerSplitClass: 2,
  result: 'PASS',
}, null, 2));
