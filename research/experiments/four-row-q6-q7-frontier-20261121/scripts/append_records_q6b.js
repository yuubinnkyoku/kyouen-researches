// append_records_q6b.js — third q=6 band extension for the K1177 frontier
// records.jsonl: (4,32,6) and (4,33,6) def-mode UNSAT, raising the published
// witness-free band from 16..31 to 16..33 (M_{4,6} = 16 or the open interval
// [34,103]). Same generator as the published extensions: genfast3
// (md5 12c2bd9cb3b24887fc3896f7ea9bcadf, core sat2.js
// md5 282ae832efa0080127c6c153e65e1c3c), calibrated byte-identically against
// the published (4,31,6) record (cnf_md5 7c6acc085ddf1820b4742bd2c47286a6).
// Both widths were solved twice with the pinned kissat 4.0.4 linux-amd64
// (md5 3a5eba830aa6008a604fcc9bbe99a325); conflicts are bit-exact across the
// double runs and match the values recorded in the research log:
//   m=32: 4,272,621 conflicts (292.77s / 295.78s process time, rc=20)
//   m=33: 4,410,392 conflicts (328.25s / 323.28s process time, rc=20)
// Runs were uncapped (sec_cap null, nohup byte-identical rerun policy).
// Fail-closed: refuses on any duplicate tag, on an input that is not exactly
// 114 records, on any mismatch against the live artifacts in output/q6ext3/,
// and on disagreement between the two independent solve logs per width.
'use strict';
const fs = require('fs');
const [, , inPath, outPath, liveDir] = process.argv;
const GEN = 'genfast3.js-md5-12c2bd9cb3b24887fc3896f7ea9bcadf-core-sat2.js-md5-282ae832efa0080127c6c153e65e1c3c';
// calibration pin: byte-identity of the genfast3 CNF with the published sat2-era record
const CALIB = { m: 31, curves: 866, vars: 19246, clauses: 66931, cnf_md5: '7c6acc085ddf1820b4742bd2c47286a6', conflicts: 3492659 };
// (m, vars, clauses, curves, cnf_md5, gen_sec, conflicts, run1_sec, run2_sec, ts)
const rows = [
  [32, 20609, 71672, 929, '65255d9825276d268219c5eaa2854959', 0.1, 4272621, 292.77, 295.78, '2026-11-21T04:26:17Z'],
  [33, 21972, 76413, 992, 'bf058f40f6bd70a4f00ddfdf72f01f72', 0.1, 4410392, 328.25, 323.28, '2026-11-21T04:26:17Z'],
];
const lines = fs.readFileSync(inPath, 'utf8').split('\n').filter(l => l.trim());
if (lines.length !== 114) { console.error('refuse: expected exactly 114 input records, got ' + lines.length); process.exit(1); }
const recs = lines.map(l => JSON.parse(l));
const tags = new Set(recs.map(r => r.tag));
for (const [m] of rows) {
  const tag = 's4x' + m + 'q6_def';
  if (tags.has(tag)) { console.error('refuse: ' + tag + ' already present'); process.exit(1); }
}
// parent-of-band schema check: the published (4,31,6) UNSAT record must match the calibration pin
const p31 = recs.find(r => r.tag === 's4x' + CALIB.m + 'q6_def');
if (!p31 || p31.kissat.result !== 'UNSATISFIABLE' || p31.kissat.rc !== 20 || p31.kissat.conflicts !== CALIB.conflicts ||
    p31.vars !== CALIB.vars || p31.clauses !== CALIB.clauses || p31.curves !== CALIB.curves ||
    p31.cnf_md5 !== CALIB.cnf_md5)
  { console.error('refuse: s4x31q6_def parent record does not match the calibration pin'); process.exit(1); }
function checkLog(fn, m, conflicts, sec) {
  const log = fs.readFileSync(fn, 'utf8');
  if (!new RegExp('c conflicts:[ ]+' + conflicts + '[ ]').test(log)) throw new Error('conflicts mismatch ' + fn);
  if (log.indexOf('s UNSATISFIABLE') < 0) throw new Error('verdict missing ' + fn);
  if (!/rc=20\s*$/.test(log)) throw new Error('rc missing ' + fn);
  if (log.indexOf(sec + ' seconds') < 0) throw new Error('seconds mismatch ' + fn);
  return true;
}
// verify every appended value against the published live artifacts (gen meta + double solve logs)
for (const [m, vars, clauses, curves, , , conflicts, r1, r2] of rows) {
  const meta = JSON.parse(fs.readFileSync(liveDir + '/gen_4x' + m + 'q6_def.json', 'utf8'));
  if (meta.w !== 4 || meta.m !== m || meta.q !== 6 || meta.mode !== 'deficient' ||
      (meta.lex || []).length !== 0 || meta.vars !== vars || meta.clauses !== clauses ||
      meta.curves !== curves)
    { console.error('refuse: gen meta mismatch m=' + m); process.exit(1); }
  checkLog(liveDir + '/solve_4x' + m + 'q6_def.txt', m, conflicts, r1);
  checkLog(liveDir + '/solve_4x' + m + 'q6_def_run2.txt', m, conflicts, r2);
}
// append (field order and types byte-match the published schema; sec_cap null = uncapped)
const out = lines.slice();
for (const [m, vars, clauses, curves, md5, gen_sec, conflicts, r1, , ts] of rows) {
  const rec = {
    w: 4, m: m, q: 6, mode: 'deficient', rowY: null, generator: GEN,
    vars: vars, clauses: clauses, curves: curves, cnf_md5: md5,
    gen_sec: gen_sec, gen_extra: '',
    kissat: { result: 'UNSATISFIABLE', rc: 20, conflicts: conflicts, sec_cap: null, sec: r1 },
    ts: ts, witness: null, tag: 's4x' + m + 'q6_def', cnf_deleted: true,
  };
  out.push(JSON.stringify(rec));
}
fs.writeFileSync(outPath, out.join('\n') + '\n');
console.log(JSON.stringify({ input_records: lines.length, output_records: out.length, appended: rows.length, bit_exact_double_runs: true }));
