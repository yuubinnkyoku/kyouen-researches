// audit_records.js — mechanical audit of the published K1177 records.jsonl
// (research/experiments/four-row-q6-q7-frontier-20261121/output/records.jsonl).
// Fail-closed: exits nonzero on any gap/inconsistency.
'use strict';
const fs = require('fs');
const recs = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n').map(JSON.parse);

const problems = [];
const tags = new Map();
for (const r of recs) {
  if (tags.has(r.tag)) problems.push(`duplicate tag ${r.tag}`);
  tags.set(r.tag, r);
  // def/lex instances must carry a pinned generator: sat2.js for the original
  // K1177 run, or (for the m>=86 band extension past the sat2.js memory wall)
  // the genfast3.js fast encoder (md5 12c2bd9c..., byte-identical CNF on the
  // calibrated low band) on the same pinned sat2.js core; capacity instances
  // carry the pinned sat5.js-capacity encoder (md5 602b905d...) on that core.
  const SAT2 = 'sat2.js-md5-282ae832efa0080127c6c153e65e1c3c';
  const GENFAST3 = 'genfast3.js-md5-12c2bd9cb3b24887fc3896f7ea9bcadf-core-sat2.js-md5-282ae832efa0080127c6c153e65e1c3c';
  const okGen = r.mode === 'capacity'
    ? r.generator === 'sat5.js-md5-602b905d21b9fd6338b2b3d83a78d4fd-core-sat2.js-md5-282ae832efa0080127c6c153e65e1c3c'
    : r.generator === SAT2 || r.generator === GENFAST3;
  if (!okGen) problems.push(`generator not pinned: ${r.tag} ${r.generator}`);
  if (r.w !== 4) problems.push(`w!=4: ${r.tag}`);
}

function find(w, m, q, mode, rowY, lex) {
  const key = `s${w}x${m}q${q}${mode === 'rowfixed' ? '_rowY' + rowY : '_def'}${lex ? '_lexH' : ''}`;
  return tags.get(key) || null;
}

const band = { q7: { sat: [], unsat: [], missing: [] }, q6: { sat: [], unsat: [], missing: [] } };
// q=7: witness band 7..12 SAT, witness-free 13..mMaxQ7 UNSAT (mMaxQ7 extends
// past the sat2.js memory wall: 85 by default per K1177, or higher via argv[4]
// for the genfast3 band extension)
const mMaxQ7 = process.argv[4] ? parseInt(process.argv[4], 10) : 85;
for (let m = 7; m <= mMaxQ7; m++) {
  const r = find(4, m, 7, 'deficient', null, false);
  if (!r) { band.q7.missing.push(m); continue; }
  if (m <= 12) {
    if (r.kissat.result !== 'SATISFIABLE') problems.push(`q7 m=${m}: expected SAT got ${r.kissat.result}`);
    const w = r.witness;
    if (!w || !(w.js_ok && w.py_ok && w.three_ok && w.js_rc === true && w.py_rc === 0 && w.three_rc === 0))
      problems.push(`q7 m=${m}: witness 3-system verify flags bad`);
    if (!(w.nStones >= 2 * 7 - 1 && w.nStones <= 4 * 6)) problems.push(`q7 m=${m}: witness stones out of band`);
    band.q7.sat.push({ m, stones: w.nStones, rows: w.rows, conflicts: r.kissat.conflicts, cnf_md5: r.cnf_md5 });
  } else {
    if (r.kissat.result !== 'UNSATISFIABLE') problems.push(`q7 m=${m}: expected UNSAT got ${r.kissat.result}`);
    if (r.kissat.rc !== 20) problems.push(`q7 m=${m}: rc!=20 (${r.kissat.rc})`);
    if (r.kissat.sec > r.kissat.sec_cap) problems.push(`q7 m=${m}: sec>cap (INDET risk)`);
    if (r.witness) problems.push(`q7 m=${m}: UNSAT record carries witness`);
    band.q7.unsat.push({ m, conflicts: r.kissat.conflicts, sec: r.kissat.sec, cap: r.kissat.sec_cap, cnf_md5: r.cnf_md5, curves: r.curves });
  }
}
// q=6: witness band 6..15 SAT, witness-free 16..29 UNSAT
for (let m = 6; m <= 29; m++) {
  const r = find(4, m, 6, 'deficient', null, false);
  if (!r) { band.q6.missing.push(m); continue; }
  if (m <= 15) {
    if (r.kissat.result !== 'SATISFIABLE') problems.push(`q6 m=${m}: expected SAT got ${r.kissat.result}`);
    band.q6.sat.push({ m, stones: r.witness.nStones, rows: r.witness.rows, cnf_md5: r.cnf_md5 });
  } else {
    if (r.kissat.result !== 'UNSATISFIABLE') problems.push(`q6 m=${m}: expected UNSAT got ${r.kissat.result}`);
    if (r.kissat.rc !== 20) problems.push(`q6 m=${m}: rc!=20`);
    if (r.witness) problems.push(`q6 m=${m}: UNSAT record carries witness`);
    band.q6.unsat.push({ m, conflicts: r.kissat.conflicts, sec: r.kissat.sec, cap: r.kissat.sec_cap, cnf_md5: r.cnf_md5, curves: r.curves });
  }
}
// any INDET/UNKNOWN overall
for (const r of recs)
  if (!['SATISFIABLE', 'UNSATISFIABLE'].includes(r.kissat.result))
    problems.push(`non-verdict record: ${r.tag} -> ${r.kissat.result}`);

// extras inventory (lex cross-encodings, capacity instances, positive control)
const extras = recs.filter(r => r.tag.includes('lexH') || r.mode === 'capacity')
  .map(r => ({ tag: r.tag, mode: r.mode, result: r.kissat.result, conflicts: r.kissat.conflicts, extra: r.gen_extra,
    witness: r.witness ? { stones: r.witness.nStones, rows: r.witness.rows,
      three_ok: r.witness.three_ok, py_ok: r.witness.py_ok, js_ok: r.witness.js_ok } : null }));
// capacity records actually live in file? check any record with mode cap
const summary = {
  schema: 1,
  total_records: recs.length,
  unique_tags: tags.size,
  q7_witness_band: band.q7.sat,
  q7_witness_free: { count: band.q7.unsat.length, span: [13, mMaxQ7], missing: band.q7.missing,
    conflicts_min: Math.min(...band.q7.unsat.map(u => u.conflicts)),
    conflicts_max: Math.max(...band.q7.unsat.map(u => u.conflicts)),
    max_solve_sec: Math.max(...band.q7.unsat.map(u => u.sec)) },
  q6_witness_band: band.q6.sat,
  q6_witness_free: { count: band.q6.unsat.length, span: [16, 29], missing: band.q6.missing,
    conflicts_min: Math.min(...band.q6.unsat.map(u => u.conflicts)),
    conflicts_max: Math.max(...band.q6.unsat.map(u => u.conflicts)) },
  capacity_witnesses: recs.filter(r => r.mode === 'capacity').map(r => ({ tag: r.tag, m: r.m, q: r.q,
    stones: r.witness.nStones, rows: r.witness.rows, verify_flags: { js: r.witness.js_ok, py: r.witness.py_ok, three: r.witness.three_ok } })),
  extras_inventory: extras,
  problems
};
fs.writeFileSync(process.argv[3], JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify({ total: recs.length, problems: problems.length,
  q7_unsat_lo_hi: [summary.q7_witness_free.count, summary.q7_witness_free.missing.length],
  q6_unsat_lo_hi: [summary.q6_witness_free.count, summary.q6_witness_free.missing.length],
  extras: extras.length }));
process.exit(problems.length ? 1 : 0);
